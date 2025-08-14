"""
UI Functions
"""

import os

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
        print("2. Edit an entry")
        print("3. Search through entries")
        print("4. View passwords again")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == "1":
            print("Returning to main menu...\n")
            break
        elif choice == "2":
            edit_password(vault,key)
        elif choice == "3":
            search_passwords(vault,key)
        elif choice =="4":
            continue
        else:
            print("Invalid choice. Please select 1-4.\n")


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
    if not vault.entries:
        print("No passwords to edit.\n")
        return
    
    while True:
        print("\n" + "="*60)
        print("EDIT PASSWORDS")
        print("="*60)
        
        print("Enter the website name or entry number to edit")
        print("Or type 'Q' to quit to main menu")
        
        entry_input = input("\nEnter website name/number: ").strip()
        
        if entry_input.upper() == "Q":
            print("Returning to main menu...\n")
            break
        
        try:
            entry_num = int(entry_input) - 1
            if 0 <= entry_num < len(vault.entries):
                entry_to_edit = vault.entries[entry_num]
            else:
                print("Invalid entry number.")
                continue
        except ValueError:
            entry_to_edit = None
            for entry in vault.entries:
                if entry_input.lower() == entry.website.lower():
                    entry_to_edit = entry
                    break
            
            if not entry_to_edit:
                print(" Website not found.")
                continue
        
        print(f"\nEditing: {entry_to_edit.website}")
        print("="*40)
        
        website = input(f"Website ({entry_to_edit.website}): ").strip() or entry_to_edit.website
        username = input(f"Username ({entry_to_edit.username}): ").strip() or entry_to_edit.username
        password = input("New password (leave blank to keep current): ").strip()
        
        entry_to_edit.website = website
        entry_to_edit.username = username
        
        if password:
            entry_to_edit.password = encrypt_password(password, key)
        
        notes_option = input("Update notes? (Y/n): ")
        if notes_option.lower() in ['y', 'yes']:
            new_notes = input("Enter new notes: ")
            entry_to_edit.notes = new_notes
        
        vault.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_vault(vault)
        
        print(f"\n Successfully updated {entry_to_edit.website}!")
        break


def delete_password(vault,key):
    if not vault.entries:
        print("No passwords to delete.\n")
        return
    
    while True:
        print("\n" + "="*60)
        print("DELETE AN ENTRY")
        print("="*60)

        print("Enter the website name or entry number to delete")
        print("Or type 'Q' to quit to main menu")
        
        entry_input = input("\nEnter website name/number: ").strip()
        
        if entry_input.upper() == "Q":
            print("Returning to main menu...\n")
            break
        
        try:
            entry_num = int(entry_input) - 1
            if 0 <= entry_num < len(vault.entries):
                entry_to_delete = vault.entries[entry_num]
            else:
                print("Invalid entry number.")
                continue
        except ValueError:
            entry_to_delete = None
            for entry in vault.entries:
                if entry_input.lower() == entry.website.lower():
                    entry_to_delete = entry
                    break
            
            if not entry_to_delete:
                print("Website not found.")
                continue
        
        print(f"\nEntry to delete: {entry_to_delete.website}")
        print("="*40)
        decrypted_password = decrypt_password(entry_to_delete.password, key)
        print(f"Website: {entry_to_delete.website}")
        print(f"Username: {entry_to_delete.username}")
        print(f"Password: {decrypted_password}")
        if entry_to_delete.notes:
            print(f"Notes: {entry_to_delete.notes}")
        print("-" * 40)
        
        confirm = input(f"\nAre you sure you want to delete {entry_to_delete.website}? (Y/n): ")
        if confirm.lower() in ['y', 'yes']:
            vault.entries.remove(entry_to_delete)
            vault.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_vault(vault)
            print(f"Successfully deleted {entry_to_delete.website}!")
        else:
            print("Deletion cancelled.")
        
        print("\nOptions:")
        print("1. Go back to main menu")
        print("2. Delete another entry")
        
        choice = input("\nSelect option (1-2): ")
        
        if choice == "1":
            print("Returning to main menu...\n")
            break
        elif choice == "2":
            continue
        else:
            print("Invalid choice. Please select 1-2.\n")

        
    
def search_passwords(vault,key):
    while True:
        print("\n" + "="*60)
        print("Search through Entries")
        print("="*60)

        print("Enter the website name or entry number to search")
        print("Or type 'Q' to quit to main menu")
        
        entry_input = input("\nEnter website name/number: ").strip()
    
        
        if entry_input.upper() == "Q":
            print("Returning to main menu...\n")
            break
        
        try:
            print(f"\nSearching for: {entry_input}")
            entry_num = int(entry_input) - 1
            if 0 <= entry_num < len(vault.entries):
                entry_to_show = vault.entries[entry_num]
            else:
                print("Invalid entry number.")
                continue
        except ValueError:
            entry_to_show = None
            for entry in vault.entries:
                if entry_input.lower() == entry.website.lower():
                    entry_to_show = entry
                    break
            
            if not entry_to_show:
                print(" Website not found.")
                continue
        
        print(f"\nEntry found: {entry_to_show.website}")
        print("="*40)
        decrypted_password = decrypt_password(entry_to_show.password, key)
        print(f"Website: {entry_to_show.website}")
        print(f"Username: {entry_to_show.username}")
        print(f"Password: {decrypted_password}")
        if entry_to_show.notes:
            print(f"Notes: {entry_to_show.notes}")
        print("-" * 40)
        
        print("\nOptions:")
        print("1. Go back to main menu")
        print("2. Search again")
        
        choice = input("\nSelect option (1-2): ")
        
        if choice == "1":
            print("Returning to main menu...\n")
            break
        elif choice == "2":
            continue
        else:
            print("Invalid choice. Please select 1-2.\n")


    
def quit_app(vault,key):
    print("Goodbye!")
    exit()


def clear_screen(vault, key):
    os.system('cls' if os.name == 'nt' else 'clear')
