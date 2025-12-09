# Legacy SegWit Bitcoin Address Generator

A Flask-based application that generates compressed legacy Bitcoin addresses from a configurable range of hex keys, with automatic page traversal, watchlist matching, and visited page/match tracking.

## Features

- **Compressed Legacy Addresses**: Generates P2PKH Bitcoin addresses from hex private keys
- **Configurable Hex Key Range**: Set start and end hex keys in `config.py`
- **Random Page Navigation**: Intelligently selects random pages within the configured range
- **Watchlist Matching**: Automatically detects and logs matched watchlist addresses
- **Auto-Reload**: Automatically navigates through pages and stops when a match is found
- **Persistent Tracking**: 
  - Visited pages logged to `data/visited_pages.txt`
  - Matched addresses logged to `data/matched_addresses.txt` with timestamp
- **Full-Page Load Detection**: Waits for complete page load before auto-navigation

## Requirements

- Python 3.8+
- Flask 2.3.3
- ecdsa 0.18.0
- base58 2.1.1
- Other dependencies in `requirements.txt`

## Installation

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd legacy-segwit-adds

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5001`

## Configuration

Edit `config.py` to customize:

```python
# Number of addresses per page
ADDRESSES_PER_PAGE = 15750

# Hex key range to search
HEX_KEY_START = 0x400000000000000000
HEX_KEY_END = 0x7fffffffffffffffff

# Flask settings
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True  # Set to False in production
```

## Watchlist

Add Bitcoin addresses to monitor in `watchlist.txt` (one address per line):

```
1A1z7agoat7cBWqvvEj9DfBoKsH8eMw...
1dice8EMCdqyqqqqqqqqqqqqqqqqqqqqqqqqqq...
```

## File Structure

```
.
├── app.py                 # Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
├── models/
│   └── all_key.py       # AllKey data model
├── services/
│   ├── all_key_service.py      # Key generation logic
│   ├── watchlist_service.py    # Watchlist matching
│   └── tracking_service.py     # File-based tracking
├── templates/
│   ├── base.html        # Base template with auto-navigation
│   ├── home.html        # Main page
│   ├── search.html      # Search page
│   ├── about.html       # About page
│   └── watchlist.html   # Watchlist management
└── data/
    ├── visited_pages.txt       # Log of visited pages
    └── matched_addresses.txt   # Log of matched addresses
```

## Data Tracking

The application now uses **SQLite database** for persistent tracking of visited pages and matched addresses.

### Database Structure

**VisitedPages Table:**
- `id` (Integer, Primary Key)
- `page_number` (String, Unique) - The page number visited
- `visited_at` (DateTime) - Timestamp when page was visited

**MatchedAddresses Table:**
- `id` (Integer, Primary Key)
- `timestamp` (DateTime) - When the match was found
- `page_number` (String) - The page containing the match
- `address` (String) - The matched Bitcoin address
- `private_key` (String) - The corresponding private key (hex)

### Database File
- Location: `data/tracking.db`
- Format: SQLite 3
- Persists across application restarts both locally and on Vercel
- Automatically created on first run

### Database Operations

Database operations are handled by `services/database_service.py`:
- `add_visited_page(page_number)` - Record a visited page
- `get_visited_pages()` - Get list of all visited pages
- `clear_visited_pages()` - Clear all visited page records
- `add_matched_address(page_number, address, private_key)` - Log a matched address
- `get_matched_addresses()` - Get all matched addresses with timestamps
- `clear_matched_addresses()` - Clear all matched address records

## Auto-Navigation Configuration

In `templates/base.html`, adjust these settings:

```javascript
const AUTO_CLICK_RANDOM = true;    // Enable/disable auto-navigation
const AUTO_CLICK_DELAY = 1000;     // Delay between page changes (milliseconds)
```

**Auto-navigation stops automatically when a watchlist match is found.**

## Deployment on Vercel

### Prerequisites

1. GitHub account with repository
2. Vercel account (https://vercel.com)
3. **Supabase account (https://supabase.com)** - Free tier available!
4. Git installed locally

### Why Supabase?

- **Persistent Database**: Data persists across Vercel deployments
- **Free Tier**: 500 MB storage, unlimited API requests
- **PostgreSQL**: Same powerful database as paid services
- **Easy Setup**: Takes 5 minutes to get connection string

### Get Supabase Connection String

1. Sign up at https://supabase.com (free)
2. Create a new project
3. Go to **Settings** → **Database**
4. Copy the **Connection string (URI)**
5. If password has `@`, replace with `%40` in the URI

Example: `postgresql://postgres:password%40123@db.xxx.supabase.co:5432/postgres`

### Step 1: Initialize Git and Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Add Supabase PostgreSQL integration for persistent database"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel with Supabase

#### Option A: Using Vercel Web Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Paste your GitHub repo URL and import
4. **Before clicking Deploy**, go to **Settings** → **Environment Variables**
5. Add environment variable:
   - **Name**: `DATABASE_URL`
   - **Value**: (Paste your Supabase connection string with `%40` for `@`)
6. Click "Deploy"

#### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy (will prompt for environment variables)
vercel

# Add environment variable when prompted:
# DATABASE_URL = postgresql://postgres:password%40...
```

### Environment Variable Setup in Vercel

**Critical**: The app looks for `DATABASE_URL` environment variable on Vercel.

Steps:
1. Go to your Vercel project → Settings
2. Environment Variables
3. Click "Add" and fill:
   - **Name**: `DATABASE_URL`
   - **Value**: `postgresql://postgres:YOUR_PASSWORD%40XX@db.dtgynqmsazbdhgvhpiwz.supabase.co:5432/postgres`
4. Select **Production** environment
5. Click "Save"
6. **Redeploy** your project for changes to take effect

### Local Development (SQLite)

When running locally without `DATABASE_URL` environment variable:
- App automatically uses SQLite (`data/tracking.db`)
- Full persistence across restarts
- No setup needed!

Test locally:
```bash
source .venv/bin/activate
python app.py
# Database uses data/tracking.db automatically
```

### Important Notes

1. **Data Persistence**: 
   - ✅ Persists across Vercel deployments
   - ✅ Persists across all requests
   - ✅ Data is in Supabase cloud servers

2. **Cold Starts**: 
   - First request may take 1-2 seconds
   - This is normal Vercel serverless behavior

3. **Database Limits** (Free Tier): 
   - 500 MB storage
   - 25 concurrent connections
   - Sufficient for this application

4. **Troubleshooting**:
   - **"could not translate host name"**: Check connection string format and URL encoding
   - **"too many connections"**: Hit connection limit; upgrade Supabase
   - **Data not persisting**: Verify `DATABASE_URL` is set in Vercel environment variables

### Database Architecture

**Local**: SQLite (`data/tracking.db`)
**Production (Vercel)**: PostgreSQL (Supabase)

Both use the same SQLAlchemy ORM models, so switching between them is seamless.

## Development

### Running Tests

```bash
# (Tests can be added here)
python -m pytest
```

### Code Structure

- **app.py**: Flask routes and request handling
- **services/**: Business logic (address generation, tracking, etc.)
- **models/**: Data classes
- **templates/**: HTML templates with JavaScript

## License

MIT License

## Support

For issues or questions, please create a GitHub issue.

## Changelog

### v2.1.0
- Added Supabase PostgreSQL support for persistent cloud database
- Automatic environment detection (SQLite local, PostgreSQL on Vercel)
- Updated deployment guide with Supabase setup instructions
- Configuration now supports DATABASE_URL environment variable

### v2.0.0
- Implemented SQLite database for persistent tracking
- Replaced file-based tracking with DatabaseService
- Improved data integrity and query capabilities
- Database tables: VisitedPages and MatchedAddresses

### v1.0.0
- Initial release
- Compressed legacy address generation
- Configurable hex key range
- Auto-navigation with watchlist matching
- File-based tracking of pages and matches
