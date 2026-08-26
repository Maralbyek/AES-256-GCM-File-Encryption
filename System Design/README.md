# AES-Based Secure File Encryption and Decryption Tool - System Design

## Project Information

| | |
|---|---|
| **Student Name** | Maralbyek Tilyek |
| **Course** | Cryptography Essentials CCC2243 |
| **Project Type** | Individual Project |
| **Year / Semester** | Year 2, Semester 3, 2025-2026 |

---

## Overview

This document presents the system design for a secure file encryption and decryption desktop application. The tool uses password-derived encryption keys and authenticated encryption to protect files. The design translates cryptographic concepts from the project proposal into an implementable application structure.

The proposed system uses:
- **Python** as the programming language
- **Tkinter** for the graphical user interface
- **PBKDF2-HMAC-SHA256** for password-based key derivation
- **AES-256-GCM** for authenticated encryption

The system is designed for single-user operation on a single computer and does not require cloud storage, network transmission, or a separate key-management server.

---

## System Architecture

The application follows a layered logical structure:

| Layer | Main Responsibility |
|-------|---------------------|
| **Presentation Layer** | Tkinter GUI, file selection, password entry, progress/status messages |
| **Application Layer** | Workflow control, validation, temporary-file handling, success/failure decisions |
| **Cryptographic and File Layer** | PBKDF2, AES-GCM, secure random generation, encrypted file formatting and parsing |

---

## System Requirements

### Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR1 | File Selection | Allow user to select a file through a file-picker dialog |
| FR2 | Password Input | Accept a password and mask password characters in the interface |
| FR3 | Password Confirmation | Request password confirmation to reduce typing errors |
| FR4 | Encryption | Derive an AES-256 key and encrypt the selected file using AES-GCM |
| FR5 | Encrypted File Creation | Create a separate encrypted output file with a .enc extension |
| FR6 | Decryption | Decrypt an encrypted file after successful authentication |
| FR7 | Integrity Verification | Reject incorrect password or modified encrypted data |
| FR8 | Output Protection | Avoid creating final decrypted output until authentication succeeds |
| FR9 | Status Messages | Display clear success and error messages |
| FR10 | Error Handling | Handle missing files, invalid formats, permission errors without crashing |

### Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Security | Use AES-256-GCM, random salts, fresh nonces, and PBKDF2-HMAC-SHA256 |
| Usability | Provide a simple graphical interface understandable by non-technical users |
| Reliability | Successful encryption and decryption shall preserve file contents exactly |
| Performance | Implementation shall be evaluated across multiple file sizes |
| Maintainability | Cryptographic operations shall be separated from the GUI |
| Portability | Application shall run on supported Python 3.10+ environments |

---

## System Design Diagrams

Three diagrams describe the system from different perspectives:

1. **Use Case Diagram** - Shows what the user can do with the system
2. **Data Flow Diagram** - Shows how information moves between processes and data storage
3. **Application Flow Diagram** - Shows the sequence of operations and decisions during encryption and decryption

---

## Encryption Process Design

| Step | Description |
|------|-------------|
| **Step 1** | User selects a source file and enters a password twice. Application checks file exists and passwords match. |
| **Step 2** | A cryptographically secure random 16-byte salt is generated. |
| **Step 3** | PBKDF2-HMAC-SHA256 processes the password and salt to produce a 32-byte AES key. |
| **Step 4** | A fresh 12-byte nonce is generated for the AES-GCM operation. |
| **Step 5** | Plaintext file bytes are encrypted using AES-256-GCM, producing ciphertext and a 16-byte authentication tag. |
| **Step 6** | Application writes version/metadata, salt, nonce, authentication tag, and ciphertext to the output file. |
| **Step 7** | Encrypted file is saved separately; original file remains unchanged. |

---

## Decryption Process Design

| Step | Description |
|------|-------------|
| **Step 1** | User selects an encrypted .enc file and enters the password. |
| **Step 2** | Application validates the file header and extracts salt, nonce, authentication tag, and ciphertext. |
| **Step 3** | Password and stored salt are passed through PBKDF2-HMAC-SHA256 using stored derivation parameters. |
| **Step 4** | AES-GCM verifies the authentication tag while decrypting the ciphertext. |
| **Step 5** | If authentication succeeds, plaintext is written to destination. If authentication fails, error is shown and no decrypted file is created. |

---

## Cryptographic Design

### Password and Key Derivation
- User password is not used directly as the AES key
- PBKDF2-HMAC-SHA256 transforms password into a 32-byte key
- New random salt generated for each encryption operation
- Password is never stored in the encrypted file

### AES-256-GCM
- Provides both confidentiality and authentication
- AES uses a 256-bit key
- GCM produces an authentication tag to detect modification

### Salt and Nonce Generation
- Generated using a cryptographically secure random-number source
- 16-byte salt and 12-byte nonce
- Fresh values generated for every encryption operation

### Authentication Tag
- Security-critical value stored with encrypted data
- Must be supplied unchanged during decryption
- Verification failure indicates incorrect password or modified ciphertext

---

## Encrypted File Format

The encrypted file uses a self-contained binary structure:

| Field | Size | Purpose |
|-------|------|---------|
| Magic / Version | Variable | Identifies file type and format version |
| PBKDF2 Parameters | Variable | Stores parameters required to reproduce key derivation |
| Salt | 16 bytes | Used with password to derive the AES key |
| Nonce | 12 bytes | Required for AES-GCM operation |
| Authentication Tag | 16 bytes | Used to verify ciphertext authenticity |
| Ciphertext | Variable | Encrypted contents of the original file |

---

## User Interface Design

| Component | Design |
|-----------|--------|
| Main Window | Provides clear choices for Encrypt and Decrypt operations |
| File Selection | Uses a file-picker dialog and displays selected filename/path |
| Password Entry | Uses masked input; encryption includes password confirmation |
| Progress/Status Area | Shows current operation without exposing cryptographic secrets |
| Result Messages | Reports successful completion or failure reason |
| Output Selection | Allows user to choose where resulting file is saved |

---

## Error Handling and Security Controls

| Condition / Risk | Control |
|------------------|---------|
| Wrong Password | AES-GCM authentication failure returns general decryption failure; no plaintext output created |
| Modified Ciphertext | Authentication fails and encrypted file is rejected |
| Malformed File | Header and length validation performed before cryptographic processing |
| Missing Source File | Application reports file cannot be accessed |
| Permission Error | User-friendly message displayed |
| Interrupted Write | Temporary output used; final file created only after successful completion |
| Password Exposure | Password values masked and not stored in encrypted file or logs |
| Accidental Overwrite | Confirmation requested before overwriting existing destination |

---

## Testing and Evaluation Design

| Test | Method | Expected Result |
|------|--------|-----------------|
| Round-trip test | Encrypt then decrypt file, compare SHA-256 hashes | Original and decrypted hashes match |
| Wrong password | Attempt decryption with incorrect password | Authentication fails; no plaintext produced |
| Tampered ciphertext | Modify ciphertext bytes | Authentication fails |
| Tampered tag | Modify authentication tag | Authentication fails |
| Different file types | Test TXT, PDF, images, archives | All files decrypt correctly |
| File sizes | Test small and large files | Operations complete without corruption |
| Missing file | Remove input before operation | Clear error, no crash |

---

## Design Limitations

- Academic desktop prototype, not an enterprise key-management platform
- No password recovery
- No cloud integration
- No multi-user access control
- No hardware security module support
- No protection against attackers who control an unlocked running system
- Security depends heavily on password quality

---

## References

- Dworkin, M. (2007). Recommendation for block cipher modes of operation: Galois/Counter Mode (GCM) and GMAC (NIST SP 800-38D)
- Kaliski, B. (2017). PKCS #5: Password-based cryptography specification version 2.1 (RFC 8018)
- National Institute of Standards and Technology. (2001). Advanced Encryption Standard (AES) (FIPS PUB 197)
- National Institute of Standards and Technology. (2010). Recommendation for password-based key derivation (NIST SP 800-132)
- OWASP Foundation. Cryptographic storage cheat sheet
- OWASP Foundation. Password storage cheat sheet
- Python Cryptographic Authority. Authenticated encryption with associated data (AEAD)
