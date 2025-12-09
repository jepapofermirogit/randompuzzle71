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

### Visited Pages
File: `data/visited_pages.txt`
- One page number per line
- No duplicates recorded

### Matched Addresses
File: `data/matched_addresses.txt`
- Format: `TIMESTAMP | Page: PAGE_NUMBER | Address: ADDRESS | PrivateKey: HEX_KEY`
- Automatically created when a watchlist address match is found

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
3. Git installed locally

### Step 1: Initialize Git and Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Bitcoin address generator with auto-navigation"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/legacy-segwit-adds.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Deploy
vercel

# Follow the prompts to:
# - Connect your GitHub account
# - Select your repository
# - Configure settings
```

#### Option B: Using Vercel Web Dashboard

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Paste your GitHub repo URL
4. Vercel will auto-detect it's a Python/Flask project
5. Click "Deploy"

### Environment Variables for Vercel

If needed, add environment variables in Vercel dashboard:

- `FLASK_ENV=production`
- Any other custom settings

### Important Notes for Vercel

1. **File Storage**: 
   - Vercel is serverless and doesn't persist files between deployments
   - `data/visited_pages.txt` and `data/matched_addresses.txt` will be reset on redeploy
   - Consider using a database or cloud storage for persistent tracking

2. **Cold Starts**: 
   - First request may take longer due to serverless cold start
   - This is normal behavior

3. **Memory Limits**: 
   - Vercel has memory limits; very large address batches may hit limits
   - Adjust `ADDRESSES_PER_PAGE` if needed

4. **Timeout**: 
   - Requests timeout after 60 seconds
   - Vercel doesn't support indefinite running processes

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

### v1.0.0
- Initial release
- Compressed legacy address generation
- Configurable hex key range
- Auto-navigation with watchlist matching
- File-based tracking of pages and matches
