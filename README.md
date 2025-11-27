# 📦 CSE 469 – Blockchain Chain of Custody (bchoc)

A **Track 1 (Programming Language-Based)** project implementing a secure, file-based blockchain for managing forensic evidence chain of custody.  
Written in **Python 3**, this command-line tool (`bchoc`) supports full evidence lifecycle management, integrity verification, and audit-ready logging.

---

## 👥 Group Members

| Name | Role |
|------|------|
| Tariq Bahaaaldeen | Developer |
| Abhinav Ranish | Developer |
| Raiden Ison | Developer |
| Hansel Kunaseelan Nadar | Developer |

---

## 📘 Overview

`bchoc` maintains a tamper-evident blockchain log for forensic evidence.  
All transactions (add, check-in, check-out, remove, etc.) are appended as immutable blocks, ensuring strong auditability.

The system supports **10 core commands**, covering the entire chain-of-custody lifecycle.

---

## 🔧 Implemented Commands

| Command        | Description                                               | Password Required |
|----------------|-----------------------------------------------------------|-------------------|
| `init`         | Creates a new blockchain with a Genesis block             | No                |
| `add`          | Adds one or more evidence items to a case                 | Creator           |
| `checkout`     | Checks out an item (CHECKEDIN → CHECKEDOUT)              | Owner             |
| `checkin`      | Checks in an item (CHECKEDOUT → CHECKEDIN)               | Owner             |
| `remove`       | Removes an item (only when CHECKEDIN)                    | Creator           |
| `show cases`   | Lists all case IDs in the blockchain                     | No                |
| `show items`   | Lists all items associated with a case                   | No                |
| `show history` | Displays full chronological history of an item           | No                |
| `verify`       | Validates blockchain integrity via hash chain            | No                |
| `summary`      | Displays counts of items by state                        | Police            |

---

## ▶️ How to Run

This project is designed for **Linux** (Ubuntu 18.04+ recommended).

---

### 1️⃣ Build the Executable

```bash
make
```

This ensures the `./bchoc` script is executable.

---

### 2️⃣ Set Environment Variables

All system passwords must be exported before running commands:

```bash
export BCHOC_PASSWORD_CREATOR="C67C"
export BCHOC_PASSWORD_POLICE="P80P"
export BCHOC_PASSWORD_ANALYST="A65A"
export BCHOC_PASSWORD_LAWYER="L76L"
export BCHOC_PASSWORD_EXECUTIVE="E69E"
```

---

### 3️⃣ Specify Blockchain File Path

Every command must be supplied with the blockchain location:

```
BCHOC_FILE_PATH="chain.db" ./bchoc <command> <args>
```

---

## 📝 Usage Examples

### Initialize the blockchain
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc init
```

### Add an evidence item
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc add \
  -c "0b711606-090e-40fb-8f9a-b82347a43887" \
  -i 3463648746 \
  -g "creator1" \
  -p "C67C"
```

### Verify blockchain integrity
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc verify
```

### Show a summary for a case
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc summary \
  -c "0b711606-090e-40fb-8f9a-b82347a43887" \
  -p "P80P"
```

---

## 📂 Project Structure (Example)

```
bchoc/
├── bchoc               # Main executable
├── blockchain.py       # Blockchain logic
├── block.py            # Block structure & hashing
├── utils.py            # Helper functions
├── Makefile            # Build script
└── README.md           # Project documentation
```

---

## 🔐 Security Features

- File-based immutable blockchain  
- SHA-256 hashing of every block  
- Strict password-protected operations  
- Chronological ordering enforcement  
- Full transaction audit logs  

---

## 🛠️ Requirements

| Dependency | Version |
|------------|----------|
| Python     | 3.6+     |
| Linux      | Ubuntu 18.04+ |
| Make       | GNU Make |

---

## 📜 License

This project was created for **CSE 469 – Computer and Network Forensics** coursework.  

---

