# 📦 CSE 469 – Blockchain Chain of Custody (`bchoc`)

A **Track 1 (Programming Language-Based)** project implementing a secure, file-based blockchain for managing forensic evidence chain of custody.  
Written in **Python 3**, this command-line tool (`bchoc`) supports full evidence lifecycle management, integrity verification, and audit-ready logging.

---

## 👥 Group Members

| Name                       | Role      |
|----------------------------|-----------|
| Tariq Bahaaaldeen          | Developer |
| Abhinav Ranish             | Developer |
| Raiden Ison                | Developer |
| Hansel Kunaseelan Nadar    | Developer |

---

## 📘 Overview

`bchoc` maintains a **tamper-evident blockchain log** for forensic evidence.

Each operation on evidence (add, check-in, check-out, removal, etc.) is recorded as an **append-only block** in a binary file.  
This ensures:

- Chronological integrity
- Detectable tampering (via hash chain)
- Audit-ready history for each evidence item and case

Internally, case IDs and item IDs are **encrypted (AES)** before being written to the blockchain file.

---

## 🔧 Implemented Commands & Password Rules

> Passwords are checked using environment variables, not passed as usernames.

### Roles & Passwords

These environment variables must be set:

- `BCHOC_PASSWORD_CREATOR` → used for:
  - `add`
  - `remove`
- Owner roles (any of these can act as “owner”):
  - `BCHOC_PASSWORD_POLICE`
  - `BCHOC_PASSWORD_LAWYER`
  - `BCHOC_PASSWORD_ANALYST`
  - `BCHOC_PASSWORD_EXECUTIVE`

### Command Summary

| Command        | Description                                                      | Password Requirement                               |
|----------------|------------------------------------------------------------------|----------------------------------------------------|
| `init`         | Create a new blockchain file with an `INITIAL` (genesis) block   | None                                               |
| `add`          | Add one or more evidence items to a case as `CHECKEDIN`          | **Creator password**                               |
| `checkout`     | Change an item from `CHECKEDIN` → `CHECKEDOUT`                   | **Owner role password**                            |
| `checkin`      | Change an item from `CHECKEDOUT` → `CHECKEDIN`                   | **Owner role password**                            |
| `remove`       | Mark an item as `DISPOSED`, `DESTROYED`, or `RELEASED`           | **Creator password**                               |
| `show cases`   | List all case IDs present in the blockchain                      | Password optional (if given, must be owner role)   |
| `show items`   | List all item IDs belonging to a specified case                  | Password optional (if given, must be owner role)   |
| `show history` | Show chronological history of blocks (optional filters)          | **Owner role password required**                   |
| `verify`       | Verify the hash chain and logical item state transitions         | None                                               |
| `summary`      | Show per-state counts of items for a given case                  | Password optional (if given, must be owner role)   |

> **Owner roles** are: POLICE, LAWYER, ANALYST, EXECUTIVE (i.e., any of their passwords).

---

## ▶️ How to Build & Run

This project is designed for **Linux** (Ubuntu recommended).

### 1️⃣ Install Dependencies

Python 3 and `pip` must be installed. Dependencies are listed in the `packages` file:

```bash
pip install -r packages
