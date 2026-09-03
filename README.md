# AES-256-GCM File Encryption Tool

## App is live here
https://aes-256-gcm-file-encryption-ejbg.onrender.com/
## Project Overview

A local desktop application for securely encrypting and decrypting files using AES-256-GCM authenticated encryption. This project demonstrates the practical application of modern symmetric cryptography through a user-friendly graphical interface, bridging the gap between cryptographic theory and usable end-user applications.

## Project Information

| | |
|---|---|
| **Student** | Maralbyek Tilyek |
| **Course** | Cryptography Essentials |

---

## Current Progress

- [x] Project Proposal
- [x] Literature Review
- [x] System Design
- [x] Implementation
- [x] Testing and Evaluation
- [ ] Final Documentation

---

## Problem Statement

Despite the availability of strong, standardized encryption, most everyday users rely on inadequate protection for sensitive files: hiding files in obscure folders, using OS-level password prompts that do not encrypt underlying data, or using archive tools with weak ciphers. None of these provide genuine confidentiality against attackers with direct storage access.

Many freely available "AES encryption" tools implement the algorithm incorrectly:
- Using ECB mode (leaks structural patterns in plaintext)
- Deriving keys directly from passwords without proper key derivation
- Omitting integrity/authentication mechanisms

This project addresses these issues by implementing a correctly engineered encryption tool that ordinary users can operate without cryptographic expertise.

---

## Aim

To design, implement, and evaluate a user-friendly desktop tool that encrypts and decrypts files using AES-256-GCM with a password-derived key, providing confidentiality, tamper detection, and password-based authentication in a single self-contained application.

---

## Objectives

| # | Objective |
|---|-----------|
| 1 | Research and document AES, symmetric cryptography, PBKDF2, and authenticated encryption |
| 2 | Design complete application workflow with diagrams |
| 3 | Implement secure key derivation using PBKDF2-HMAC-SHA256 with per-file salt |
| 4 | Implement AES-256-GCM encryption with unique random nonces |
| 5 | HTML, CSS, and JavaScript, served locally by a Python HTTP server with file selection, masked password entry, and status messages |
| 6 | Test systematically across file types, sizes, and security scenarios |
| 7 | Document design, implementation, threat model, and test results |

---

## Key Features

### Encryption
- Select any file via file-picker dialog
- Enter and confirm password (masked input)
- Automatic salt and nonce generation
- Outputs encrypted file with `.enc` extension
- Original file remains unchanged

### Decryption
- Select encrypted `.enc` file
- Enter the password used for encryption
- Automatic integrity verification
- Original file reconstructed only if authentication succeeds

### Security
- Incorrect passwords rejected
- Tampered ciphertext detected and rejected
- Modified authentication tags cause decryption failure
- No decrypted output unless authentication passes
- Passwords never stored

---

## Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Programming Language | Python 3.10+ | Application development |
| GUI Framework | HTML, CSS, JS | Graphical user interface |
| Cryptography Library | Python cryptography package | AES-GCM and PBKDF2 operations |
| Encryption | AES-256-GCM | Authenticated encryption |
| Key Derivation | PBKDF2-HMAC-SHA256, 480,000 iterations | Password to AES key conversion |
| Salt | 16 bytes (random per encryption) | Prevents precomputation attacks |
| Nonce | 12 bytes (fresh per encryption) | Ensures unique encryption contexts |
| Authentication Tag | 16 bytes | Verifies file integrity |
| Testing | pytest | Unit and integration tests |
| Version Control | Git and GitHub | Source code management |

---

## Architecture

The application follows a layered logical structure:

| Layer | Responsibility |
|-------|----------------|
| **Presentation Layer** | HTML, CSS, JS GUI, file selection, password entry, progress/status messages |
| **Application Layer** | Workflow control, validation, temporary-file handling, success/failure decisions |
| **Cryptographic Layer** | PBKDF2, AES-GCM, secure random generation |
| **File Layer** | Encrypted file formatting and parsing |

---

## Encryption Workflow

| Step | Description |
|------|-------------|
| **Step 1** | User selects a source file and enters a password twice. Application checks file exists and passwords match. |
| **Step 2** | A cryptographically secure random 16-byte salt is generated. |
| **Step 3** | PBKDF2-HMAC-SHA256 processes the password and salt (480,000 iterations) to produce a 32-byte AES key. |
| **Step 4** | A fresh 12-byte nonce is generated for the AES-GCM operation. |
| **Step 5** | Plaintext file bytes are encrypted using AES-256-GCM, producing ciphertext and a 16-byte authentication tag. |
| **Step 6** | Application writes version/metadata, salt, nonce, authentication tag, and ciphertext to the output file. |
| **Step 7** | Encrypted file is saved separately with `.enc` extension; original file remains unchanged. |

---

## Decryption Workflow

| Step | Description |
|------|-------------|
| **Step 1** | User selects an encrypted `.enc` file and enters the password. |
| **Step 2** | Application validates the file header and extracts salt, nonce, authentication tag, and ciphertext. |
| **Step 3** | Password and stored salt are passed through PBKDF2-HMAC-SHA256 using stored derivation parameters. |
| **Step 4** | AES-GCM verifies the authentication tag while decrypting the ciphertext. |
| **Step 5** | If authentication succeeds, plaintext is written to destination. If authentication fails, error is shown and no decrypted file is created. |

---

## Encrypted File Format

The encrypted output is a self-contained binary file. No separate key file is required.

| Field | Size | Purpose |
|-------|------|---------|
| Magic / Version | Variable | Identifies file type and format version |
| PBKDF2 Parameters | Variable | Key derivation parameters (iteration count, etc.) |
| Salt | 16 bytes | Used with password to derive AES key |
| Nonce | 12 bytes | Required for AES-GCM operation |
| Authentication Tag | 16 bytes | Verifies ciphertext authenticity |
| Ciphertext | Variable | Encrypted contents of the original file |

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

## Threat Model

The design assumes an attacker who may obtain a full copy of the encrypted file (e.g., stolen laptop or leaked backup) but does not have access to the password and cannot observe application memory during use.

| Risk | Mitigation |
|------|------------|
| Weak/reused user passwords | Password-strength indicator; recommendation of passphrase length |
| Nonce reuse | Fresh key (via new salt) + fresh random nonce per encryption |
| Interrupted/corrupted writes | Write to temporary file; rename only on successful completion |
| Tampered ciphertext | Authentication tag verification prevents undetected modification |

---

## User Interface Design

| Component | Design |
|-----------|--------|
| Main Window | Provides clear choices for Encrypt and Decrypt operations |
| File Selection | Uses a file-picker dialog and displays selected filename/path |
| Password Entry | Uses masked input; encryption includes password confirmation |
| Progress/Status Area | Shows current operation without exposing cryptographic secrets |
| Result Messages | Reports successful completion or general failure reason |
| Output Selection | Allows user to choose where resulting file is saved |

---

## Error Handling and Security Controls

| Condition / Risk | Control |
|------------------|---------|
| Wrong Password | AES-GCM authentication failure; no plaintext output created |
| Modified Ciphertext | Authentication fails; encrypted file rejected |
| Malformed File | Header and length validation before cryptographic processing |
| Missing Source File | Clear error message displayed |
| Permission Error | User-friendly message instead of unexpected termination |
| Interrupted Write | Temporary output used; final file created only after successful completion |
| Password Exposure | Password values masked; not stored in encrypted file or logs |
| Accidental Overwrite | Confirmation requested before overwriting existing destination |

---

## Testing and Evaluation

| Test Category | Method | Expected Result |
|---------------|--------|-----------------|
| Correctness | Encrypt then decrypt file, compare SHA-256 hashes | Original and decrypted hashes match |
| Security - Wrong Password | Attempt decryption with incorrect password | Authentication fails; no plaintext produced |
| Security - Tampered Ciphertext | Modify one or more ciphertext bytes | Authentication fails |
| Security - Tampered Tag | Modify the authentication tag | Authentication fails |
| Usability | Test user unfamiliar with tool | Encrypt and decrypt without external instructions |
| Performance | Measure across file sizes (1 KB to 500 MB) | Target: under 5 seconds for 100 MB file |
| Robustness - Missing File | Remove input before operation | Clear error, no crash |
| Robustness - Different Types | Test TXT, PDF, images, archives | All files decrypt correctly |

---

## Scope

### In Scope
- Local, single-user file encryption and decryption on a single computer
- Support for common file types (text documents, PDFs, images, compressed archives)
- Self-contained encrypted output files (no separate key file needed)
- Graphical interface for non-technical users

### Out of Scope
- Cloud storage integration or network transmission
- Multi-user account management or access control
- Password recovery (forgotten password = unrecoverable file)
- Enterprise key management or HSM integration
- Protection against memory/side-channel attacks

---

## Design Option Comparison

| Option | Strengths | Decision |
|--------|-----------|----------|
| AES-GCM | Encryption and tamper detection in one standard mode | **Selected** |
| AES-CBC + MAC | Well-known confidentiality mode | Not selected (more complex) |
| AES-128 | Strong security, lower cost | Not selected (smaller security margin) |
| AES-256 | Large key space, strong security margin | **Selected** |
| Direct password use | Simple to explain and code | **Rejected** (unsafe) |
| PBKDF2 (480k iterations) | Standardized, slows guessing | **Selected** |

---

## Project Structure

```text
AES-256-GCM-File-Encryption/
│
├── Project Proposal/
│   ├── AES_File_Encryption_Tool_Project_Proposal.pdf
│   └── README.md
│
├── Literature Review/
│   ├── AES_File_Encryption_Tool_Literature_Review.pdf
│   └── README.md
│
├── System Design/
│   ├── PDF/
│   │   ├── Figure1_UseCaseDiagram.drawio.pdf
│   │   ├── Figure2_DataFlowDiagram.drawio.pdf
│   │   └── Figure3_ApplicationWorkflow.drawio.pdf
│   │
│   ├── XML/
│   │   ├── Figure1_UseCaseDiagram.drawio.xml
│   │   ├── Figure2_DataFlowDiagram.drawio.xml
│   │   └── Figure3_ApplicationWorkflow.drawio.xml
│   │
│   ├── AES_Secure_File_Encryption_System_Design_Report.pdf
│   └── README.md
│
├── Implementation/
│   └── Code/
│       ├── aes_tool/
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── crypto_engine.py
│       │   └── database.py
│       ├── frontend/
│       │   ├── index.html
│       │   ├── app.js
│       │   └── styles.css
│       ├── tests/
│       │   └── test_crypto_engine.py
│       ├── aes_vault.db
│       └── Launch AES Vault.vbs
│
├── Testing and Evaluation/
│   └── (test reports)
│
├── Final Report/
│   └── (final documentation)
│
└── README.md
