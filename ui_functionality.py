"""
UI Functions
"""

from models import PasswordEntry
from vault import save_vault
from datetime import datetime


def display_passwords(vault):
    print("Displaying passwords...")

def add_password(vault):
    accepted_inputs = ["Y",'y','Yes','YES']

    website = input("Website:")
    username = input("Username:")
    password = input("Password:")
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

def edit_password(vault):
    print("Editing password...")

def delete_password(vault):
    print("Deleting password...")
    

def search_passwords(vault):
    print("Searching passwords...")

def quit_app(vault):
    print("Goodbye!")
    exit()
