#!/usr/bin/env python3

"""
Simple Terminal Password Manager
Features: Master password protection, 3-attempt limit, 10-minute lockout
"""

from getpass import getpass
from crypto import hash_master_password, generate_salt, verify_master_password
from vault import create_vault, save_vault, vault_exists, load_vault


def build_ui():
    pass


def main():
    """Main entry point."""
    
    if not vault_exists():
        print("Creating a vault...")
        
        while True:
            master_password = getpass("Create your master password: ")
            if len(master_password) < 6:
                print("Password must be at least 6 characters long.")
                continue
                
            confirm = getpass("Confirm your master password: ")
            if master_password != confirm:
                print("Passwords don't match. Try again.")
                continue
            break
        
        vault = create_vault(master_password)
        save_vault(vault)
        print("Vault successfully created!")
        
    else:
        vault = load_vault()
    
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        print(f"Attempts remaining: {max_attempts - attempts}")
        password_attempt = getpass("Enter master password: ")
        
        if verify_master_password(vault, password_attempt):
            print("Access granted!")
            build_ui()
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print("Invalid password. Try again.")
            else:
                print("Too many failed attempts. Goodbye!")


if __name__ == "__main__":
    main()
    