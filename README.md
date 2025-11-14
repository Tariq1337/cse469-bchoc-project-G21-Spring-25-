# CSE 469: Blockchain Chain of Custody (bchoc)

A Track 1 (Programming Language-Based) solution for the CSE 469 group project.  
This command-line tool, **bchoc**, implements a secure, file-based blockchain used to record the *chain of custody* for digital forensic evidence.

The program is written in **Python 3**.

---

## 👥 Group Member(s)

- **[YOUR NAME]** (ASU ID: **[YOUR ASU ID]**)  
- *(Add additional group members here)*

---

## 📌 Program Description

This project provides a full implementation of all 10 required blockchain-based custody commands:

### 🔧 Core Commands
| Command | Description |
|--------|-------------|
| **init** | Creates a new blockchain file with a Genesis block. |
| **add** | Adds one or more evidence items (requires *creator* password). |
| **checkout** | Checks out an item (state: CHECKEDIN → CHECKEDOUT, owner password required). |
| **checkin** | Checks in an item (state: CHECKEDOUT → CHECKEDIN, owner password required). |
| **remove** | Removes an item (requires creator password & item must be CHECKEDIN). |
| **show cases** | Displays all unique case IDs in the blockchain. |
| **show items** | Displays all items belonging to a specific case. |
| **show history** | Shows the full chronological history for an item. |
| **verify** | Verifies the blockchain hash integrity. |
| **summary** | Prints counts of items by state for a given case. |

Each operation appends a new block, ensuring traceability, integrity, and tamper-evidence.

---

## 🚀 How to Run

The tool is intended for **Linux** (Ubuntu 18.04+ recommended).

### 1. 🛠 Build the Executable

Ensure the `bchoc` script is executable using the provided `Makefile`:

```bash
make
```

---

### 2. 🔐 Set Required Environment Variables

All passwords **must be read from environment variables**, following project specifications:

```bash
export BCHOC_PASSWORD_CREATOR="C67C"
export BCHOC_PASSWORD_POLICE="P80P"
export BCHOC_PASSWORD_ANALYST="A65A"
export BCHOC_PASSWORD_LAWYER="L76L"
export BCHOC_PASSWORD_EXECUTIVE="E69E"
```

---

### 3. ▶️ Run the Program

You must specify the blockchain file path using:

```
BCHOC_FILE_PATH="path/to/chain.db"
```

Here are example commands:

#### Initialize a new chain:
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc init
```

#### Add an evidence item:
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc add \
    -c "0b711606-090e-40fb-8f9a-b82347a43887" \
    -i 3463648746 \
    -g "creator1" \
    -p "C67C"
```

#### Verify blockchain integrity:
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc verify
```

#### Show a case summary:
```bash
BCHOC_FILE_PATH="chain.db" ./bchoc summary \
    -c "0b711606-090e-40fb-8f9a-b82347a43887" \
    -p "P80P"
```

---

## 🤖 Generative AI Acknowledgment

Portions of this project were created with assistance from Google's Gemini language model.

**Reference:**  
Google. (2024). *Gemini* [Large language model].

---

## 📄 License

*(Add license information if required.)*
