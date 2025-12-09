"""
Configuration settings for the All Bitcoin Private Key application
"""

# Number of addresses to display per page
ADDRESSES_PER_PAGE = 15750

# Hex key range configuration
HEX_KEY_START = 0x400000000000000000  # Starting hex key range
HEX_KEY_END = 0x7fffffffffffffffff    # Ending hex key range

# Performance options
MAX_SEARCH_PAGES = 200   # Maximum pages to search through for address lookup (reduced for Vercel)

# API configuration - Optimized for Vercel serverless
API_REQUEST_DELAY = 0.5   # seconds between API requests (increased for stability)
API_CHUNK_SIZE = 25       # addresses per API request (reduced to avoid URL length issues)
API_MAX_THREADS = 2       # maximum concurrent threads (reduced for Vercel)

# Bitcoin configuration
BITCOIN_MAX_NUMBER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140

# Flask configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True  # Set to True for development (auto-reload templates)

# Database configuration
import os

# Check if running on Vercel or if DATABASE_URL is provided
if os.environ.get('DATABASE_URL'):
    # Use PostgreSQL (Supabase) for production
    # Use connection pooler for serverless environments (Vercel)
    db_url = os.environ.get('DATABASE_URL')
    
    # Convert to use connection pooler if it's a Supabase URL
    if 'supabase.co' in db_url:
        # Replace the port with connection pooler port and add ?sslmode=require
        db_url = db_url.replace(':5432', ':6543') + '?sslmode=require'
    
    SQLALCHEMY_DATABASE_URI = db_url
    
    # Connection pooling settings for serverless
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'connect_args': {
            'connect_timeout': 10,
        }
    }
else:
    # Use SQLite locally
    _db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    _db_path = os.path.join(_db_dir, 'tracking.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{_db_path}'
    SQLALCHEMY_ENGINE_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = False

