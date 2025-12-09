"""
Database service for managing visited pages and matched addresses
"""

from models.database import db, VisitedPage, MatchedAddress
from datetime import datetime
import os


class DatabaseService:
    """Service to handle database operations for tracking"""
    
    @staticmethod
    def init_db(app):
        """Initialize database with Flask app"""
        # Create data directory if it doesn't exist
        # Extract path from SQLite URI (e.g., 'sqlite:///data/tracking.db' -> 'data')
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///data/tracking.db')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            data_dir = os.path.dirname(db_path)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
        
        with app.app_context():
            db.init_app(app)
            db.create_all()
    
    @staticmethod
    def add_visited_page(page_number):
        """Add a visited page to the database"""
        try:
            # Check if page already exists
            existing = VisitedPage.query.filter_by(page_number=str(page_number)).first()
            if existing:
                return False  # Already visited
            
            # Add new visited page
            visited_page = VisitedPage(page_number=str(page_number))
            db.session.add(visited_page)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error adding visited page: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_visited_pages():
        """Get all visited pages"""
        try:
            pages = VisitedPage.query.all()
            return [page.page_number for page in pages]
        except Exception as e:
            print(f"Error retrieving visited pages: {e}")
            return []
    
    @staticmethod
    def clear_visited_pages():
        """Clear all visited pages"""
        try:
            VisitedPage.query.delete()
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error clearing visited pages: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def add_matched_address(page_number, address, private_key):
        """Add a matched address to the database"""
        try:
            matched = MatchedAddress(
                page_number=str(page_number),
                address=address,
                private_key=private_key
            )
            db.session.add(matched)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error adding matched address: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_matched_addresses():
        """Get all matched addresses"""
        try:
            matches = MatchedAddress.query.order_by(MatchedAddress.timestamp.desc()).all()
            return [match.to_dict() for match in matches]
        except Exception as e:
            print(f"Error retrieving matched addresses: {e}")
            return []
    
    @staticmethod
    def clear_matched_addresses():
        """Clear all matched addresses"""
        try:
            MatchedAddress.query.delete()
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error clearing matched addresses: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def count_visited_pages():
        """Get count of visited pages"""
        try:
            return VisitedPage.query.count()
        except Exception as e:
            print(f"Error counting visited pages: {e}")
            return 0
    
    @staticmethod
    def count_matched_addresses():
        """Get count of matched addresses"""
        try:
            return MatchedAddress.query.count()
        except Exception as e:
            print(f"Error counting matched addresses: {e}")
            return 0
