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

# Determine database URL
if os.environ.get('DATABASE_URL'):
    # Supabase provided - use it
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') + '?sslmode=require'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 1,
        'max_overflow': 0,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'connect_args': {
            'connect_timeout': 5,
        }
    }
else:
    # Fall back to SQLite locally or on Vercel if DATABASE_URL not set
    # Note: On Vercel, data persists only during the current request
    # For persistent storage, please set DATABASE_URL to Supabase connection string
    if os.environ.get('VERCEL'):
        # On Vercel without DATABASE_URL, use /tmp for temporary storage
        _db_path = '/tmp/tracking.db'
    else:
        # Local development
        _db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        _db_path = os.path.join(_db_dir, 'tracking.db')
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{_db_path}'
    SQLALCHEMY_ENGINE_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = False

