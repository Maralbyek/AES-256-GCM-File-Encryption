# AES-Based Secure File Encryption and Decryption Tool - Project Proposal

## Project Information

| | |
|---|---|
| **Student Name** | Maralbyek Tilyek |
| **Student ID** | AIU24102280 |
| **Course** | Cryptography Essentials CCC2243 |
| **Project Type** | Individual Project |
| **Year / Semester** | Year 2, Semester 3, 2025-2026 |

---

## Background

Digital files containing sensitive information (academic transcripts, financial statements, medical records, source code) are vulnerable when stored on laptops, removable drives, or shared network locations. Encryption addresses this by transforming plaintext into ciphertext that is infeasible to reverse without the correct key.

The Advanced Encryption Standard (AES) is the symmetric-key block cipher standardized by NIST in FIPS PUB 197 (2001). It has become the global standard for protecting data at rest. This project applies AES in its authenticated Galois/Counter Mode (AES-GCM) to build a practical file encryption tool with a simple graphical interface.

---

## Problem Statement

Most everyday users rely on inadequate protection: hiding files in obscure folders, using OS-level password prompts that don't encrypt data, or using archive tools with weak ciphers. None of these provide genuine confidentiality.

Many freely available "AES encryption" tools implement the algorithm incorrectly:
- Using ECB mode (leaks structural patterns)
- Deriving keys directly from passwords without a proper KDF
- Omitting integrity/authentication mechanisms

There is a need for a correctly engineered application that gives ordinary users access to properly implemented AES encryption without requiring cryptographic expertise.

---

## Aim

To design, implement, and evaluate a user-friendly desktop tool that encrypts and decrypts files using AES-256-GCM with a password-derived key, providing confidentiality, tamper detection, and password-based authentication.

---

## Objectives

| # | Objective |
|---|-----------|
| 1 | Research and document AES, symmetric cryptography, PBKDF2, and authenticated encryption |
| 2 | Design the complete application workflow with diagrams |
| 3 | Implement secure key derivation using PBKDF2-HMAC-SHA256 with per-file salt and 480,000+ iterations |
| 4 | Implement AES-256-GCM encryption with unique random nonces and authentication verification |
| 5 | Build a Tkinter GUI with file selection, masked password entry, and clear status messages |
| 6 | Test systematically across file types, sizes, correct/incorrect passwords, and corrupted ciphertext |
| 7 | Document design, implementation, threat model, test results, and limitations |

---

## Project Scope

### In Scope
- Local, single-user file encryption and decryption
- Support for common file types (TXT, PDF, images, archives)
- Self-contained encrypted output files (no separate key file needed)

### Out of Scope
- Cloud storage or network transmission
- Multi-user access control
- Password recovery (forgotten password = unrecoverable file)
- Enterprise key management or HSM integration
- Protection against memory/side-channel attacks

---

## Proposed Methodology

### Encryption Workflow
1. User selects file and enters password (confirmed twice)
2. Generate random 16-byte salt
3. Derive 256-bit AES key using PBKDF2-HMAC-SHA256 (480,000+ iterations)
4. Encrypt with AES-256-GCM using fresh 12-byte nonce
5. Output: salt + nonce + authentication tag + ciphertext in .enc file

### Decryption Workflow
1. User selects .enc file and enters password
2. Parse salt, nonce, and authentication tag from header
3. Re-derive AES key using stored salt
4. Decrypt and verify authentication tag
5. If verification fails → abort with error, no output
6. If verification succeeds → reconstruct original file

### Threat Model

Assumes attacker may obtain encrypted file but not password and cannot observe application memory during use.

| Risk | Mitigation |
|------|------------|
| Weak/reused passwords | Password strength indicator; encourage passphrase length |
| Nonce reuse | Fresh key (via new salt) + fresh random nonce per encryption |
| Interrupted/corrupted writes | Write to temporary file; rename only on successful completion |

---

## Tools and Technologies

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.10+ |
| GUI | Tkinter |
| Cryptography Library | Python cryptography package |
| Encryption | AES-256-GCM |
| Key Derivation | PBKDF2-HMAC-SHA256, 480,000+ iterations, random salt |
| Testing | pytest |
| Version Control | Git and GitHub |
| Documentation | Markdown, draw.io, Microsoft Word |

---

## Expected Outcome

A working graphical application for encrypting and decrypting arbitrary files. Encrypted output reveals no information about original content. Incorrect passwords or modified ciphertext fail with clear error messages. Decrypted files are byte-for-byte identical to originals. Performance target: under 5 seconds for a 100 MB file.

---

## Testing and Evaluation Criteria

| Category | Criteria |
|----------|----------|
| Correctness | Round-trip reproduces original file (SHA-256 hash comparison) |
| Security | Incorrect password rejected; modified ciphertext/tag fails authentication |
| Usability | Non-technical user can encrypt/decrypt without external instructions |
| Performance | Measured and reported across file sizes (1 KB to 500 MB) |
| Robustness | Handles missing files, permission errors, interruptions without crashing |

---

## Proposed Work Schedule

| Stage | Deliverable | Weight |
|-------|-------------|--------|
| 1 | Project Proposal | 5% |
| 2 | Literature Review | 10% |
| 3 | System Design | 10% |
| 4 | Implementation | 30% |
| 5 | Testing and Evaluation | 15% |
| 6 | Final Report | 20% |
| 7 | Presentation and Demonstration | 10% |

---

## Conclusion

This project will demonstrate how modern authenticated symmetric cryptography can be applied correctly to protect files against disclosure and tampering. By combining AES-256-GCM with properly salted, iterated PBKDF2 and grounding decisions in established standards (FIPS 197, NIST SP 800-38D, NIST SP 800-132, OWASP), the tool avoids common implementation mistakes while remaining simple enough for non-technical users.

---

## References (Preliminary)

- NIST. (2001). FIPS PUB 197 (AES)
- NIST. (2007). SP 800-38D (GCM)
- NIST. (2010). SP 800-132 (Key Derivation)
- OWASP Password Storage Cheat Sheet
- Python Cryptography Documentation
