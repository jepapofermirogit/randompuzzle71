import hashlib
import ecdsa
from ecdsa import SigningKey, SECP256k1
import base58
from models.all_key import AllKey
from config import HEX_KEY_START, HEX_KEY_END

class AllKeyService:
    """Service for generating Bitcoin private keys and compressed legacy addresses"""
    
    def __init__(self):
        self.curve = SECP256k1
    
    def get_data(self, page: int, limit_per_page: int) -> list[AllKey]:
        """Generate Bitcoin keys for a specific page within the configured range"""
        items = []
        
        for index in range(limit_per_page):
            # Calculate the key ID for this position
            key_id = (page - 1) * limit_per_page + index + 1
            
            # Check if key is within the configured range
            if key_id < HEX_KEY_START or key_id > HEX_KEY_END:
                continue
            
            # Convert to hex and pad to 64 characters (32 bytes)
            id_hex = hex(key_id)[2:]  # Remove '0x' prefix
            # Pad with zeros to make it 64 characters (32 bytes)
            id_hex = id_hex.zfill(64)
            
            # Generate only compressed legacy address
            address_compressed = self._get_address(id_hex, compressed=True)
            private_key = self._get_private_key(id_hex)
            
            items.append(AllKey(
                id=id_hex,
                private_key=private_key,
                hex_private_key=id_hex,
                address_compressed=address_compressed
            ))
        
        return items
    
    def _get_address(self, key_hex: str, compressed: bool = True) -> str:
        """Generate compressed Bitcoin legacy address from private key"""
        try:
            # Convert hex to bytes
            private_key_bytes = bytes.fromhex(key_hex)
            
            # Create signing key
            signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
            verifying_key = signing_key.get_verifying_key()
            
            # Get public key
            public_key = verifying_key.to_string()
            
            # Compressed public key (33 bytes)
            if public_key[63] % 2 == 0:
                public_key_compressed = b'\x02' + public_key[:32]
            else:
                public_key_compressed = b'\x03' + public_key[:32]
            public_key_bytes = public_key_compressed
            
            # Hash the public key
            sha256_hash = hashlib.sha256(public_key_bytes).digest()
            ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
            
            # Add version byte (0x00 for mainnet)
            versioned_payload = b'\x00' + ripemd160_hash
            
            # Calculate checksum
            checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
            
            # Create final address
            address_bytes = versioned_payload + checksum
            address = base58.b58encode(address_bytes).decode('utf-8')
            
            return address
            
        except Exception as e:
            print(f"Error generating address: {e}")
            return "Error"
    
    def _get_private_key(self, key_hex: str) -> str:
        """Generate WIF (Wallet Import Format) private key for compressed address"""
        try:
            # Convert hex to bytes
            private_key_bytes = bytes.fromhex(key_hex)
            
            # Add version byte (0x80 for mainnet)
            versioned_key = b'\x80' + private_key_bytes
            
            # Calculate checksum
            checksum = hashlib.sha256(hashlib.sha256(versioned_key).digest()).digest()[:4]
            
            # Create final private key
            private_key_bytes = versioned_key + checksum
            private_key = base58.b58encode(private_key_bytes).decode('utf-8')
            
            return private_key
            
        except Exception as e:
            print(f"Error generating private key: {e}")
            return "Error"
    

