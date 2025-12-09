from flask import Flask, render_template, request, redirect, url_for
from services.all_key_service import AllKeyService
from services.watchlist_service import WatchlistService
from services.database_service import DatabaseService
from models.database import db
from config import ADDRESSES_PER_PAGE, BITCOIN_MAX_NUMBER, FLASK_HOST, FLASK_PORT, FLASK_DEBUG, MAX_SEARCH_PAGES, HEX_KEY_START, HEX_KEY_END, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = SQLALCHEMY_ENGINE_OPTIONS

# Initialize database with app context
db.init_app(app)

# Initialize services
all_key_service = AllKeyService()
watchlist_service = WatchlistService()

# Create database tables on first request (with error handling)
_db_initialized = False

@app.before_request
def create_tables():
    global _db_initialized
    if not _db_initialized:
        try:
            db.create_all()
            _db_initialized = True
            print("✓ Database tables created/verified")
        except Exception as e:
            # Log error but continue - app will work with limited functionality
            print(f"⚠ Database warning (app will continue): {type(e).__name__}: {str(e)[:100]}")
            _db_initialized = True  # Only try once per deployment

@app.route('/')
def home():
    return redirect(url_for('home_page', page=1))

@app.route('/home')
def home_page():
    try:
        page = int(float(request.args.get('page', 1)))
    except (ValueError, TypeError):
        page = 1
    
    # Ensure page is at least 1
    page = max(1, page)
    
    limit_per_page = ADDRESSES_PER_PAGE
    
    # Get Bitcoin keys and addresses
    items = all_key_service.get_data(page, limit_per_page)
    
    # Record visited page to database
    DatabaseService.add_visited_page(page)
    
    # Check watchlist for matches
    all_addresses = []
    for item in items:
        all_addresses.append(item.address_compressed)
    
    watchlist_matches = watchlist_service.find_matching_addresses(all_addresses)
    
    # Add watchlist match indicator to items and record matches
    for item in items:
        item.is_watchlist_match_compressed = item.address_compressed in watchlist_matches
        # Record matched addresses to database
        if item.is_watchlist_match_compressed:
            DatabaseService.add_matched_address(
                page,
                item.address_compressed,
                item.hex_private_key
            )
    
    # Calculate pagination based on full Bitcoin range for proper page calculations
    max_page = BITCOIN_MAX_NUMBER // limit_per_page
    page_percentage = calculate_page_percentage(page, max_page)
    
    # Count matching addresses on this page
    matches_count = len(watchlist_matches)
    
    return render_template('home.html', 
                         items=items, 
                         page=page, 
                         max_page=max_page,
                         page_percentage=page_percentage,
                         table_header_columns=[
                             'privateKey', 'compressed'
                         ],
                         watchlist_matches=matches_count,
                         is_watchlist_empty=watchlist_service.is_empty())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/random')
def random_page():
    """Redirect to a random page within the configured hex key range"""
    import random
    import math
    
    limit_per_page = ADDRESSES_PER_PAGE
    
    # Calculate the page range that contains the configured hex keys
    start_page = HEX_KEY_START // limit_per_page
    end_page = HEX_KEY_END // limit_per_page
    
    # Pick a random page within the valid range
    random_page_num = random.randint(start_page, end_page)
    
    return redirect(url_for('home_page', page=random_page_num))

@app.route('/search')
def search():
    """Search for a specific Bitcoin address and find which page it's on"""
    address = request.args.get('address', '').strip()
    start_page = request.args.get('start_page', '1').strip()
    
    if not address:
        return render_template('search.html', error="Please enter an address to search")
    
    # Validate Bitcoin address format (basic check)
    if not (address.startswith('1') or address.startswith('3') or address.startswith('bc1')):
        return render_template('search.html', error="Invalid Bitcoin address format")
    
    # Validate and parse starting page
    try:
        start_page = int(start_page)
        if start_page < 1:
            return render_template('search.html', 
                                 address=address, 
                                 start_page=start_page,
                                 error="Starting page must be 1 or greater")
    except ValueError:
        return render_template('search.html', 
                             address=address, 
                             start_page=start_page,
                             error="Invalid starting page number")
    
    # Search for the address
    result = find_address_page(address, start_page)
    
    if result:
        return render_template('search.html', 
                             address=address, 
                             start_page=start_page,
                             page=result['page'], 
                             position=result['position'],
                             private_key=result['private_key'],
                             is_compressed=result['is_compressed'])
    else:
        return render_template('search.html', 
                             address=address, 
                             start_page=start_page,
                             error=f"Address not found in pages {start_page} to {start_page + MAX_SEARCH_PAGES - 1}")

def find_address_page(target_address, start_page=1):
    """Find which page contains a specific Bitcoin address"""
    # We need to search through the generated addresses
    # This is computationally expensive, so we'll use a smart search approach
    
    # Search through MAX_SEARCH_PAGES starting from the specified start_page
    end_page = start_page + MAX_SEARCH_PAGES - 1
    
    for page in range(start_page, end_page + 1):
        items = all_key_service.get_data(page, ADDRESSES_PER_PAGE)
        
        for i, item in enumerate(items):
            if item.address_compressed == target_address:
                return {
                    'page': page,
                    'position': i + 1,
                    'private_key': item.private_key,
                    'is_compressed': True
                }
    
    # If not found in the search range, return None
    return None

def truncate_text(text, start_chars=4, end_chars=3):
    """Truncate text to show only start and end characters with dots in between"""
    if not text or len(text) <= start_chars + end_chars:
        return text
    return f"{text[:start_chars]}..{text[-end_chars:]}"

def format_page_number(page_num):
    """Format large page numbers to be more readable"""
    try:
        # Convert to int if it's a string
        if isinstance(page_num, str):
            page_num = int(page_num)
        
        if page_num < 1000:
            return str(page_num)
        elif page_num < 1000000:
            return f"{page_num // 1000}K"
        elif page_num < 1000000000:
            return f"{page_num // 1000000}M"
        else:
            return f"{page_num // 1000000000}B"
    except (ValueError, TypeError):
        # If conversion fails, return a simplified version
        return "∞"

def format_scientific_notation(number):
    """Format large numbers in scientific notation"""
    try:
        if isinstance(number, str):
            number = int(number)
        
        if number < 1000:
            return str(number)
        else:
            # Convert to scientific notation
            import math
            exponent = int(math.log10(number))
            coefficient = number / (10 ** exponent)
            
            # Round coefficient to 2 decimal places
            coefficient = round(coefficient, 2)
            
            # Use proper superscript characters
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
            }
            
            exponent_str = ''.join(superscript_map.get(digit, digit) for digit in str(exponent))
            return f"{coefficient}×10{exponent_str}"
    except (ValueError, TypeError, OverflowError):
        # For extremely large numbers, use a fallback
        return "2.8×10²³"

def calculate_page_percentage(current_page, max_page):
    """Calculate the percentage of current page position within total pages using logarithmic scale
    
    This is essential for Bitcoin key space where max_page is ~10^76.
    Logarithmic scaling makes the percentage meaningful (order of magnitude).
    """
    import math
    
    if max_page <= 0 or current_page <= 0:
        return 0.00
    
    # Use logarithmic scale to handle massive page numbers
    # Maps: page 1 -> 0%, page at log(max_page) -> ~50%, page at max_page -> 100%
    log_current = math.log10(current_page)
    log_max = math.log10(max_page)
    
    if log_max <= 0:
        return 0.00
    
    percentage = (log_current / log_max) * 100
    # Clamp to 0-100 range
    percentage = min(100.00, max(0.00, percentage))
    return round(percentage, 2)

@app.route('/watchlist')
def watchlist():
    """View and manage watchlist"""
    watchlist_addresses = sorted(watchlist_service.get_watchlist())
    return render_template('watchlist.html', addresses=watchlist_addresses)

@app.route('/watchlist/add', methods=['POST'])
def add_to_watchlist():
    """Add address to watchlist"""
    address = request.form.get('address', '').strip()
    if address:
        watchlist_service.add_address(address)
    return redirect(url_for('watchlist'))

@app.route('/watchlist/remove', methods=['POST'])
def remove_from_watchlist():
    """Remove address from watchlist"""
    address = request.form.get('address', '').strip()
    if address:
        watchlist_service.remove_address(address)
    return redirect(url_for('watchlist'))

# Make functions available in templates
app.jinja_env.globals.update(
    truncate_text=truncate_text,
    format_page_number=format_page_number,
    format_scientific_notation=format_scientific_notation,
    calculate_page_percentage=calculate_page_percentage,
    MAX_SEARCH_PAGES=MAX_SEARCH_PAGES,
    ADDRESSES_PER_PAGE=ADDRESSES_PER_PAGE,
    HEX_KEY_START=HEX_KEY_START,
    HEX_KEY_END=HEX_KEY_END
)

# For Vercel deployment
app = app

if __name__ == '__main__':
    try:
        # Use threaded=True and use_reloader=False for better Windows compatibility
        app.run(
            debug=FLASK_DEBUG, 
            host=FLASK_HOST, 
            port=FLASK_PORT,
            threaded=True,
            use_reloader=False,
            use_debugger=FLASK_DEBUG
        )
    except Exception as e:
        print(f"Server error: {e}")