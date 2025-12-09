import os
from datetime import datetime
from pathlib import Path

class TrackingService:
    """Service for tracking visited pages and matched watchlist addresses"""
    
    def __init__(self):
        # Create data directory if it doesn't exist
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
        self.visited_pages_file = self.data_dir / 'visited_pages.txt'
        self.matched_addresses_file = self.data_dir / 'matched_addresses.txt'
    
    def add_visited_page(self, page_number):
        """Add a page number to the visited pages file"""
        try:
            # Check if page is already visited
            if self.is_page_visited(page_number):
                return
            
            with open(self.visited_pages_file, 'a') as f:
                f.write(f"{page_number}\n")
        except Exception as e:
            print(f"Error adding visited page: {e}")
    
    def is_page_visited(self, page_number):
        """Check if a page has been visited"""
        try:
            if not self.visited_pages_file.exists():
                return False
            
            with open(self.visited_pages_file, 'r') as f:
                visited_pages = f.read().strip().split('\n')
                return str(page_number) in visited_pages
        except Exception as e:
            print(f"Error checking visited page: {e}")
            return False
    
    def get_visited_pages(self):
        """Get all visited pages"""
        try:
            if not self.visited_pages_file.exists():
                return []
            
            with open(self.visited_pages_file, 'r') as f:
                content = f.read().strip()
                if content:
                    return [int(page) for page in content.split('\n') if page.strip()]
            return []
        except Exception as e:
            print(f"Error getting visited pages: {e}")
            return []
    
    def clear_visited_pages(self):
        """Clear all visited pages"""
        try:
            if self.visited_pages_file.exists():
                self.visited_pages_file.unlink()
        except Exception as e:
            print(f"Error clearing visited pages: {e}")
    
    def add_matched_address(self, address, page_number, private_key):
        """Add a matched watchlist address to the file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.matched_addresses_file, 'a') as f:
                f.write(f"{timestamp} | Page: {page_number} | Address: {address} | PrivateKey: {private_key}\n")
        except Exception as e:
            print(f"Error adding matched address: {e}")
    
    def get_matched_addresses(self):
        """Get all matched addresses"""
        try:
            if not self.matched_addresses_file.exists():
                return []
            
            with open(self.matched_addresses_file, 'r') as f:
                lines = f.read().strip().split('\n')
                return [line for line in lines if line.strip()]
        except Exception as e:
            print(f"Error getting matched addresses: {e}")
            return []
    
    def clear_matched_addresses(self):
        """Clear all matched addresses"""
        try:
            if self.matched_addresses_file.exists():
                self.matched_addresses_file.unlink()
        except Exception as e:
            print(f"Error clearing matched addresses: {e}")
