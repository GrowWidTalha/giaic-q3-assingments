import json
import os
from typing import Dict, Optional
from datetime import datetime, timedelta

class StorageManager:
    def __init__(self, storage_file: str = "secure_data.json"):
        self.storage_file = storage_file
        self.stored_data: Dict = {}
        self.failed_attempts: Dict[str, int] = {}  # Track attempts per data entry
        self.lockout_until: Dict[str, datetime] = {}  # Track lockout times
        self.load_data()
    
    def load_data(self) -> None:
        """Load data from JSON file if it exists."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    self.stored_data = json.load(f)
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            self.stored_data = {}
    
    def save_data(self) -> None:
        """Save data to JSON file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.stored_data, f)
        except Exception as e:
            print(f"Error saving data: {str(e)}")
    
    def store_data(self, data_id: str, encrypted_text: str, hashed_passkey: str) -> None:
        """Store encrypted data with its hashed passkey."""
        self.stored_data[data_id] = {
            "encrypted_text": encrypted_text,
            "passkey": hashed_passkey,
            "created_at": datetime.now().isoformat()
        }
        self.save_data()
    
    def get_data(self, data_id: str) -> Optional[Dict]:
        """Retrieve stored data by ID."""
        return self.stored_data.get(data_id)
    
    def increment_failed_attempts(self, data_id: str) -> int:
        """Increment failed attempts for a data entry."""
        self.failed_attempts[data_id] = self.failed_attempts.get(data_id, 0) + 1
        attempts = self.failed_attempts[data_id]
        
        if attempts >= 3:
            # Set lockout for 15 minutes
            self.lockout_until[data_id] = datetime.now() + timedelta(minutes=15)
        
        return attempts
    
    def reset_failed_attempts(self, data_id: str) -> None:
        """Reset failed attempts for a data entry."""
        self.failed_attempts[data_id] = 0
        self.lockout_until.pop(data_id, None)
    
    def is_locked_out(self, data_id: str) -> bool:
        """Check if a data entry is currently locked out."""
        if data_id not in self.lockout_until:
            return False
        
        if datetime.now() > self.lockout_until[data_id]:
            # Lockout period has expired
            self.lockout_until.pop(data_id)
            self.failed_attempts[data_id] = 0
            return False
        
        return True
    
    def get_remaining_lockout_time(self, data_id: str) -> Optional[timedelta]:
        """Get remaining lockout time for a data entry."""
        if data_id not in self.lockout_until:
            return None
        
        remaining = self.lockout_until[data_id] - datetime.now()
        return remaining if remaining.total_seconds() > 0 else None 