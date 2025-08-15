#!/usr/bin/env python3

"""
Simple Terminal Password Manager
Features: Master password protection, 3-attempt limit, 10-minute lockout
"""

import os

from getpass import getpass
from crypto import verify_master_password, derive_encryption_key
from vault import create_vault, save_vault, vault_exists, load_vault
from ui_functionality import (
    display_passwords, 
    add_password, 
    edit_password, 
    delete_password, 
    search_passwords, 
    quit_app,
    clear_screen
)


def build_ui(vault,key):
    """Main password management interface."""
    
    menu_actions = {
        "1": display_passwords,
        "2": add_password,
        "3": edit_password,
        "4": delete_password,
        "5": search_passwords,
        "6": clear_screen,
        "7": quit_app
    }
    
    while True:
        print("\n" + "="*50)
        print("🔐 PASSWORD VAULT")
        print("="*50)
        
        print("\n Options:")
        print("1. Display Passwords")
        print("2. Add Password")
        print("3. Edit Password") 
        print("4. Delete Password")
        print("5. Search Passwords")
        print("6. Clear Screen")
        print("7. Quit")
        
        choice = input("\nSelect option (1-7): ")
        
        if choice in menu_actions:
            clear_screen(vault,key)
            menu_actions[choice](vault,key)
        else:
            print("Invalid choice. Please select 1-7.")


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
            key=derive_encryption_key(password_attempt,vault.master_salt)
            clear_screen(vault,key)
            build_ui(vault,key)
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print("Invalid password. Try again.")
            else:
                print("Too many failed attempts. Goodbye!")


if __name__ == "__main__":
    main()
    