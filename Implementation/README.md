# AES Vault

A local browser-based file encryption and decryption tool using AES-256-GCM authenticated encryption. The application runs a Python backend locally and provides a web interface through the browser.
## Encryption

<img width="1143" height="1102" alt="image" src="https://github.com/user-attachments/assets/712ff766-15b6-4d40-a261-65ed78f01739" />

## Decryption
<img width="1143" height="1102" alt="image" src="https://github.com/user-attachments/assets/a4fe6446-6116-4322-b34c-c763129d390b" />


## Database
<img width="1312" height="784" alt="kxmlu" src="https://github.com/user-attachments/assets/0f488698-0836-4d6d-9645-ebe3b55b59b8" />





## Features

- Encrypt any file using AES-256-GCM
- Decrypt encrypted `.enc` files
- Password-based key derivation using PBKDF2-HMAC-SHA256
- Random 16-byte salt for every encryption operation
- Fresh 12-byte nonce for every encryption operation
- Authentication tag verification
- Detection of incorrect passwords and tampered files
- No plaintext output is created when authentication fails
- Temporary-file handling for safer file operations
- Local operation without cloud storage or network transmission
- Operation history stored locally in SQLite

## Technologies

| Component | Technology |
|---|---|
| Backend | Python 3.10+ |
| Web server | Python built-in HTTP server |
| Frontend | HTML, CSS, and JavaScript |
| Encryption | AES-256-GCM |
| Key derivation | PBKDF2-HMAC-SHA256 |
| Cryptography library | Python `cryptography` package |
| Database | SQLite |
| Testing | pytest |
| Launcher | Windows VBScript |

## Project Structure

```text
Code/
├── aes_tool/
│   ├── __init__.py
│   ├── app.py
│   ├── crypto_engine.py
│   └── database.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── tests/
│   └── test_crypto_engine.py
├── aes_vault.db
└── Launch AES Vault.vbs
