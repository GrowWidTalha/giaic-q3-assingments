from cryptography.fernet import Fernet
import hashlib
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class EncryptionManager:
    def __init__(self):
        # Generate a key for Fernet encryption
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        
        # Salt for PBKDF2 (in production, this should be stored securely)
        self.salt = os.urandom(16)
    
    def hash_passkey(self, passkey: str) -> str:
        """Hash passkey using PBKDF2 for enhanced security."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(passkey.encode()))
        return key.decode()
    
    def encrypt_data(self, text: str) -> str:
        """Encrypt data using Fernet symmetric encryption."""
        try:
            return self.cipher.encrypt(text.encode()).decode()
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_data(self, encrypted_text: str) -> str:
        """Decrypt data using Fernet symmetric encryption."""
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def verify_passkey(self, stored_hash: str, provided_passkey: str) -> bool:
        """Verify if the provided passkey matches the stored hash."""
        try:
            provided_hash = self.hash_passkey(provided_passkey)
            return stored_hash == provided_hash
        except Exception:
            return False 