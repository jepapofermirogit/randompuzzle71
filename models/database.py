"""
Database models for tracking visited pages and matched addresses
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class VisitedPage(db.Model):
    """Track visited pages to avoid revisiting the same page"""
    __tablename__ = 'visited_pages'
    
    id = db.Column(db.Integer, primary_key=True)
    page_number = db.Column(db.String(255), unique=True, nullable=False, index=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VisitedPage {self.page_number}>'


class MatchedAddress(db.Model):
    """Track matched addresses found in watchlist"""
    __tablename__ = 'matched_addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    page_number = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False, index=True)
    private_key = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<MatchedAddress {self.address}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'page_number': self.page_number,
            'address': self.address,
            'private_key': self.private_key
        }
