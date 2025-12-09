import os
from typing import Set, Dict, List

class WatchlistService:
    """Service for managing Bitcoin address watchlist"""
    
    def __init__(self, watchlist_file: str = 'watchlist.txt'):
        self.watchlist_file = watchlist_file
        self.watchlist: Set[str] = set()
        self.load_watchlist()
    
    def load_watchlist(self) -> None:
        """Load addresses from watchlist file"""
        self.watchlist = set()
        
        if not os.path.exists(self.watchlist_file):
            return
        
        try:
            with open(self.watchlist_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        self.watchlist.add(line.lower())
        except Exception as e:
            print(f"Error loading watchlist: {e}")
    
    def get_watchlist(self) -> Set[str]:
        """Get current watchlist"""
        return self.watchlist.copy()
    
    def add_address(self, address: str) -> bool:
        """Add an address to the watchlist"""
        address = address.strip().lower()
        if address and len(address) > 10:  # Basic validation
            self.watchlist.add(address)
            self.save_watchlist()
            return True
        return False
    
    def remove_address(self, address: str) -> bool:
        """Remove an address from the watchlist"""
        address = address.strip().lower()
        if address in self.watchlist:
            self.watchlist.remove(address)
            self.save_watchlist()
            return True
        return False
    
    def save_watchlist(self) -> None:
        """Save watchlist to file"""
        try:
            with open(self.watchlist_file, 'w') as f:
                f.write("# Bitcoin Address Watchlist\n")
                f.write("# Add one Bitcoin address per line\n")
                f.write("# Lines starting with # are comments\n\n")
                for address in sorted(self.watchlist):
                    f.write(f"{address}\n")
        except Exception as e:
            print(f"Error saving watchlist: {e}")
    
    def find_matching_addresses(self, addresses: List[str]) -> Dict[str, str]:
        """Find addresses that match the watchlist
        
        Args:
            addresses: List of addresses to check
            
        Returns:
            Dictionary with address -> matched_address mapping
        """
        matches = {}
        addresses_lower = {addr.lower(): addr for addr in addresses}
        
        for watched_addr in self.watchlist:
            if watched_addr in addresses_lower:
                matches[addresses_lower[watched_addr]] = True
        
        return matches
    
    def check_address_in_watchlist(self, address: str) -> bool:
        """Check if a single address is in the watchlist"""
        return address.lower() in self.watchlist
    
    def is_empty(self) -> bool:
        """Check if watchlist is empty"""
        return len(self.watchlist) == 0
