# AES-256-GCM File Encryption Tool

## Project Overview

A local desktop application for securely encrypting and decrypting files using AES-256-GCM authenticated encryption. This project demonstrates the practical application of modern symmetric cryptography through a user-friendly graphical interface.

## Project Information

| | |
|---|---|
| **Student** | Maralbyek Tilyek |
| **Course** | Cryptography Essentials |
| **Semester** | Year 2, Semester 3, 2025-2026 |

## Current Progress

- [x] Project Proposal
- [x] Literature Review
- [x] System Design
- [ ] Implementation
- [ ] Testing and Evaluation
- [ ] Final Documentation

## Key Features

- File encryption with AES-256-GCM
- Password-based key derivation using PBKDF2-HMAC-SHA256 (480,000 iterations)
- Random salt and nonce generation per encryption
- Integrity verification via authentication tags
- Simple graphical interface using Tkinter
- Cross-platform support (Windows, macOS, Linux)

## Technologies

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.10+ |
| GUI Framework | Tkinter |
| Cryptography Library | Python cryptography package |
| Encryption | AES-256-GCM |
| Key Derivation | PBKDF2-HMAC-SHA256 |
| Testing | pytest |
| Version Control | Git and GitHub |

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
│   │   ├── AES_Secure_File_Encryption_System_Design_Report.pdf
│   │   ├── Figure1_UseCaseDiagram.drawio.pdf
│   │   ├── Figure2_DataFlowDiagram.drawio.pdf
│   │   └── Figure3_ApplicationWorkflow.drawio.pdf
│   │
│   ├── XML/
│   │   ├── Figure1_UseCaseDiagram.drawio.xml
│   │   ├── Figure2_DataFlowDiagram.drawio.xml
│   │   └── Figure3_ApplicationWorkflow.drawio.xml
│   │
│   └── README.md
│
├── Implementation/
│   └── (source code)
│
├── Testing and Evaluation/
│   └── (test reports)
│
├── Final Report/
│   └── (final documentation)
│
└── README.md
