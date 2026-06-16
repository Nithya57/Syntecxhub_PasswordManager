import os
import sys
import json
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

VAULT_FILE = "vault.json"
SALT_FILE = "salt.bin"
ITERATIONS = 200_000


def get_or_create_salt() -> bytes:
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)



def load_vault(fernet: Fernet) -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()
    if not encrypted_data:
        return {}
    try:
        decrypted = fernet.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
    except Exception:
        print("ERROR: Incorrect master password or corrupted vault.")
        sys.exit(1)


def save_vault(fernet: Fernet, vault: dict) -> None:
    data = json.dumps(vault, indent=2).encode()
    encrypted = fernet.encrypt(data)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)



def add_entry(vault: dict) -> None:
    site = input("Site/App name: ").strip()
    username = input("Username/Email: ").strip()
    password = getpass.getpass("Password (hidden): ").strip()
    vault[site] = {"username": username, "password": password}
    print(f"Entry for '{site}' added.")


def retrieve_entry(vault: dict) -> None:
    site = input("Site/App name: ").strip()
    entry = vault.get(site)
    if entry:
        print(f"\nSite     : {site}")
        print(f"Username : {entry['username']}")
        print(f"Password : {entry['password']}\n")
    else:
        print(f"No entry found for '{site}'.")


def delete_entry(vault: dict) -> None:
    site = input("Site/App name to delete: ").strip()
    if site in vault:
        del vault[site]
        print(f"Entry for '{site}' deleted.")
    else:
        print(f"No entry found for '{site}'.")


def search_entries(vault: dict) -> None:
    keyword = input("Search keyword: ").strip().lower()
    matches = [site for site in vault if keyword in site.lower()]
    if matches:
        print("\nMatching entries:")
        for site in matches:
            print(f"  - {site}")
        print()
    else:
        print("No matching entries found.")


def list_entries(vault: dict) -> None:
    if not vault:
        print("Vault is empty.")
        return
    print("\nStored entries:")
    for site in vault:
        print(f"  - {site}")
    print()



MENU = """
========================================
   LOCAL PASSWORD MANAGER
========================================
1. Add new entry
2. Retrieve entry
3. Search entries
4. List all entries
5. Delete entry
6. Exit
========================================
"""


def main():
    print("=== Password Manager Login ===")
    master_password = getpass.getpass("Enter master password: ")

    salt = get_or_create_salt()
    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    vault = load_vault(fernet)
    print("Vault unlocked successfully.\n")

    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_entry(vault)
            save_vault(fernet, vault)
        elif choice == "2":
            retrieve_entry(vault)
        elif choice == "3":
            search_entries(vault)
        elif choice == "4":
            list_entries(vault)
        elif choice == "5":
            delete_entry(vault)
            save_vault(fernet, vault)
        elif choice == "6":
            print("Vault saved. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
