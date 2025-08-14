"""
UI Functions
"""

from models import PasswordEntry
from vault import save_vault
from datetime import datetime
from crypto import encrypt_password, decrypt_password


def display_passwords(vault,key):
    if not vault.entries:
        print("No passwords stored yet.\n")
        return
    
    while True:
        print("\n" + "="*60)
        print("STORED PASSWORDS")
        print("="*60)
        
        sorted_entries = sorted(vault.entries, key=lambda x: x.website.lower())
        
        for i, entry in enumerate(sorted_entries, 1):
            decrypted_password = decrypt_password(entry.password, key)
            print(f"{i}. Website: {entry.website}")
            print(f"   Username: {entry.username}")
            print(f"   Password: {decrypted_password}")
            if entry.notes:
                print(f"   Notes: {entry.notes}")
            print("-" * 40)
        
        print("\nOptions:")
        print("1. Go back to main menu")
        print("2. View passwords again")
        
        choice = input("\nSelect option (1-2): ")
        
        if choice == "1":
            print("Returning to main menu...\n")
            break
        elif choice == "2":
            continue
        else:
            print("Invalid choice. Please select 1-2.\n")


def add_password(vault,key):
    accepted_inputs = ["Y",'y','Yes','YES']

    website = input("Website:")
    username = input("Username:")
    password = input("Password:")
    password = encrypt_password(password,key)
    notes_option = input("Add notes? (Y/n)")
    if notes_option in accepted_inputs:
        notes = input("Enter Note:")
        new_entry= PasswordEntry(website=website,username=username,password=password,notes=notes)
        vault.entries.append(new_entry)
        vault.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        save_vault(vault)
        
    else:
        new_entry= PasswordEntry(website=website,username=username,password=password)
        vault.entries.append(new_entry)
        vault.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        save_vault(vault)

    print("Adding password...")

def edit_password(vault,key):
    

    print("Editing password...")

def delete_password(vault,key):
    print("Deleting password...")
    
def search_passwords(vault,key):
    print("Searching passwords...")

def quit_app(vault,key):
    print("Goodbye!")
    exit()
