from models import Vault, PasswordEntry
import os
import json
from datetime import datetime
from crypto import hash_master_password, generate_salt

def vault_exists():
    """Check if vault directory and vault.json file exist."""
    vault_file = "vault/vault.json"
    return os.path.exists(vault_file)

def create_vault(master_password):
    """Create a new vault for storing passwords."""
    vault_dir = "vault"  
    
    os.makedirs(vault_dir, exist_ok=True)
    
    salt = generate_salt()
    hash_result = hash_master_password(master_password, salt)
    
    vault = Vault(
        name="Password_Vault",
        master_salt=salt,
        master_hash=hash_result,
        entries=[],
        created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    return vault

def save_vault(vault):
    """Save vault to file."""
    vault_file = "vault/vault.json" 
    
    with open(vault_file, 'w') as f:
        json.dump(vault.to_dict(), f, indent=2)

def load_vault():
    """Load vault from file if it exists."""
    vault_file = "vault/vault.json" 
    
    if os.path.exists(vault_file):
        with open(vault_file, 'r') as f:
            data = json.load(f)
            return Vault.from_dict(data)
    else:
        return None


