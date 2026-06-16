# Syntecxhub_PasswordManager

A local password manager built in Python that securely stores credentials using AES encryption, protected by a master password.

## Overview

This project was built as part of the **Syntecxhub Cybersecurity Internship — Week 1, Project 2**. It demonstrates core security concepts including symmetric encryption, key derivation, and secure local data storage.

## Features

- **AES Encryption** — All credentials are encrypted using the `cryptography` library's Fernet implementation (AES-128 in CBC mode with HMAC authentication).
- **Master Password Protection** — A single master password unlocks the vault. The password itself is never stored; it is used to derive an encryption key via PBKDF2-HMAC-SHA256 (200,000 iterations) with a randomly generated salt.
- **Add Entry** — Store a new site/app along with a username and password.
- **Retrieve Entry** — Look up and decrypt a saved entry by site name.
- **Search Entries** — Search stored site names using a keyword.
- **List Entries** — View all saved site names at a glance.
- **Delete Entry** — Remove a saved entry from the vault.
- **Encrypted Storage** — All data is stored in `vault.json`, fully encrypted on disk. A separate `salt.bin` file stores the random salt used for key derivation.

## How It Works

1. On first run, you create a master password.
2. A random salt is generated and saved to `salt.bin`.
3. The master password + salt are passed through PBKDF2 to derive a secure encryption key.
4. This key is used with Fernet (AES) to encrypt/decrypt the vault contents.
5. The encrypted vault is saved to `vault.json`.

## Requirements

```
pip install cryptography
```

## Usage

```
python password_manager.py
```

Follow the on-screen menu to add, retrieve, search, list, or delete password entries.

## Security Notes

- `vault.json` and `salt.bin` are excluded from this repository to protect sensitive data — only the source code is shared.
- Losing your master password means the vault cannot be decrypted; there is no recovery mechanism by design.
- This project is for educational purposes as part of an internship program and should be reviewed before any production use.

## Tech Stack

- Python 3
- `cryptography` library (Fernet, PBKDF2HMAC)
- JSON for data structure
