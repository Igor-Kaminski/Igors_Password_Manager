"""
Encrpytion Functions
"""

from base64 import encode
import hashlib
import secrets

def hash_master_password(master_password,salt):
    return hashlib.sha256((master_password + salt).encode()).hexdigest()

def generate_salt():
    return secrets.token_hex(16)

def verify_master_password(vault, input_password):
    """Verify master password against stored hash."""
    input_hash = hash_master_password(input_password, vault.master_salt)
    return input_hash == vault.master_hash  


