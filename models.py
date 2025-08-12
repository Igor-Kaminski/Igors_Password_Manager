from dataclasses import dataclass

@dataclass
class PasswordEntry:
    """Represents a single password entry in the vault."""
    website: str
    username: str
    password: str
    notes = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "website": self.website,
            "username": self.username,
            "password": self.password,
            "notes": self.notes or ""
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary for JSON deserialization."""
        return cls(
            website=data.get("website", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            notes=data.get("notes", "")
        )

@dataclass
class Vault:
    """Represents a collection of password entries with master password."""
    name: str
    master_salt: str
    master_hash: str
    entries: list
    created_date: str
    last_modified: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "master_salt": self.master_salt,
            "master_hash": self.master_hash,
            "entries": [entry.to_dict() for entry in self.entries],
            "created_date": self.created_date,
            "last_modified": self.last_modified
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary for JSON deserialization."""
        return cls(
            name=data.get("name", ""),
            master_salt=data.get("master_salt", ""),
            master_hash=data.get("master_hash", ""),
            entries=[PasswordEntry.from_dict(entry) for entry in data.get("entries", [])],
            created_date=data.get("created_date", ""),
            last_modified=data.get("last_modified", "")
        ) 