"""
Encrpytion Functions
"""

import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def hash_master_password(master_password, salt):
    return hashlib.sha256((master_password + salt).encode()).hexdigest()

def generate_salt():
    return secrets.token_hex(16)

def derive_encryption_key(master_password, salt):
    """Derive encryption key from master password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=1_200_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def encrypt_password(password, key):
    """Encrypt a password using the master password + salt."""
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_password(encrypted_password, key):
    """Decrypt a password using the master password + salt."""
    try:
        f = Fernet(key)
        decrypted = f.decrypt(base64.urlsafe_b64decode(encrypted_password))
        return decrypted.decode()
    except:
        return None

def verify_master_password(vault, input_password):
    input_hash = hash_master_password(input_password, vault.master_salt)
    return input_hash == vault.master_hash  


