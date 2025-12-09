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
