# AES-Based Secure File Encryption and Decryption Tool - Literature Review

## Project Information

| | |
|---|---|
| **Student Name** | Maralbyek Tilyek |
| **Course** | Cryptography Essentials CCC2243 |
| **Year / Semester** | Year 2, Semester 3, 2025-2026 |

---

## Overview

This literature review examines cryptographic concepts for the proposed AES-Based Secure File Encryption and Decryption Tool, covering symmetric cryptography, AES, authenticated encryption, key derivation, salts, nonces, and secure implementation practices.

---

## Key Concepts and Design Decisions

| Concept | Description | Design Decision |
|---------|-------------|-----------------|
| **Symmetric Cryptography** | Uses same key for encryption and decryption. Faster than public-key. | Password converted to AES key using KDF with random salt. |
| **AES** | NIST-standardized block cipher (FIPS PUB 197). Supports 128/192/256-bit keys. | AES-256-GCM selected (not just AES). |
| **AES-GCM** | Authenticated encryption providing both confidentiality and integrity via 16-byte authentication tag. | Fresh 12-byte nonce per encryption. Reuse prohibited. |
| **PBKDF2** | Password-based key derivation (RFC 8018). Uses salt, iteration count, and HMAC-SHA-256. | 480,000 iterations. Salt and iteration count stored in encrypted file. |
| **File Format** | Encrypted files store salt, nonce, and authentication tag. | Structure: version header + salt + nonce + authentication tag + ciphertext. Uses .enc extension. |
| **Secure Implementation** | Small mistakes invalidate strong cryptography. | Use Python cryptography library. Mask passwords. General error messages. |

---

## Design Option Comparison

| Option | Decision |
|--------|----------|
| AES-GCM | Selected |
| AES-CBC + MAC | Not selected |
| AES-128 | Not selected |
| AES-256 | Selected |
| Direct password use | Rejected |
| PBKDF2 (480,000 iterations) | Selected |

---

## Relevance to Project

| Component | Selection |
|-----------|-----------|
| Language | Python |
| GUI | Tkinter |
| Crypto Library | cryptography package |
| Salt | 16 bytes (fresh per encryption) |
| Nonce | 12 bytes (fresh per encryption) |
| Key Derivation | PBKDF2-HMAC-SHA256, 480,000 iterations |
| Encryption | AES-256-GCM |

**Evaluation Criteria:** Correctness, Security, Robustness, Usability, Performance.

---

## Conclusion

AES-256-GCM with PBKDF2-HMAC-SHA256 (480,000 iterations) is suitable for the proposed project. Secure file encryption requires authenticated mode, unique nonces, random salts, careful file formatting, and safe error handling.

---

## References

- Dworkin, M. (2007). NIST SP 800-38D (GCM)
- Kaliski, B. (2017). RFC 8018 (PKCS #5)
- NIST. (2001). FIPS PUB 197 (AES)
- NIST. (2010). NIST SP 800-132 (Key Derivation)
- OWASP Cryptographic Storage Cheat Sheet
