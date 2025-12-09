from dataclasses import dataclass
from typing import Optional

@dataclass
class AllKey:
    """Data class representing a Bitcoin key with compressed legacy address"""
    id: str
    private_key: str
    hex_private_key: str
    address_compressed: str
