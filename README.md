# 📦 CSE 469 – Blockchain Chain of Custody (`bchoc`)

**Course:** CSE 469 – Computer and Network Forensics  
**Group 21 – Track 1 (Programming Language-Based)**

A Track 1 project implementing a secure, file-based blockchain for managing forensic evidence chain of custody.  
Written in **Python 3**, this command-line tool (`bchoc`) supports full evidence lifecycle management, integrity verification, and audit-ready logging.

---

## 👥 Group Members

| Name                    | ASU ID     |
|-------------------------|-----------:|
| Tariq Bahaaaldeen       | 1223918566 |
| Abhinav Ranish          | 1226800395 |
| Raiden Ison             | 1218779887 |
| Hansel Kunaseelan Nadar | 1224956915 |
| Ismail Wehelie          | 1224733367 |

---

## 📘 Overview

`bchoc` maintains a **tamper-evident blockchain log** for forensic evidence.

Each operation on evidence (add, check-in, check-out, removal, etc.) is recorded as an **append-only block** in a binary file:

- No blocks are ever modified in place  
- Each block’s SHA-256 hash becomes the `prev_hash` of the next block  
- Any change to historical data breaks the hash chain and is detected by `verify`

To protect IDs at rest:

- **Case IDs** (UUID strings) and **item IDs** (integers) are encrypted using **AES (ECB mode)**  
- Encrypted values are stored as hex-encoded bytes in the block header

---

## 🧱 Blockchain File & Block Layout

The program reads and writes to a single blockchain file.

- The file path is taken from the environment variable **`BCHOC_FILE_PATH`**  
- If not set, it defaults to `bchoc.db` in the current directory

Each block is a fixed-size header plus optional data:

- `prev_hash` – 32 bytes (hash of the previous block, or all zeros for the genesis block)  
- `timestamp` – 8-byte double (Unix epoch)  
- `case_id` – 32 bytes (hex-encoded AES-encrypted UUID)  
- `item_id` – 32 bytes (hex-encoded AES-encrypted 4-byte integer)  
- `state` – 12-byte string (`INITIAL`, `CHECKEDIN`, `CHECKEDOUT`, `DISPOSED`, `DESTROYED`, `RELEASED`)  
- `creator` – 12-byte string (who created the evidence)  
- `owner` – 12-byte string (current owner role on check-in/check-out)  
- `data_len` – 4-byte unsigned int  
- `data` – `data_len` bytes (optional; e.g., RELEASED owner info)

The helper module **`block_helper.py`** is responsible for:

- AES encryption/decryption of `case_id` and `item_id`  
- Packing fields into a binary header (`pack_block`)  
- Unpacking headers back into a Python dict (`unpack_block`)

The main script **`bchoc`**:

- Parses commands via `argparse` subparsers  
- Validates role passwords from environment variables  
- Computes current item state by scanning the chain (no external DB)  
- Appends new blocks while maintaining the hash chain

---

## 🔐 Roles, Passwords & Environment

Passwords are **not** usernames; they are validated against environment variables.

### Set the following before running:

```bash
export BCHOC_PASSWORD_CREATOR="C67C"
export BCHOC_PASSWORD_POLICE="P80P"
export BCHOC_PASSWORD_LAWYER="L76L"
export BCHOC_PASSWORD_ANALYST="A65A"
export BCHOC_PASSWORD_EXECUTIVE="E69E"
```

### Role Description

| Role | Purpose | Variable |
|------|---------|----------|
| **Creator** | Required for adding or removing items | `BCHOC_PASSWORD_CREATOR` |
| **Owner Roles** | Authorized to checkout/checkin items and view history | `BCHOC_PASSWORD_POLICE`, `BCHOC_PASSWORD_LAWYER`, `BCHOC_PASSWORD_ANALYST`, `BCHOC_PASSWORD_EXECUTIVE` |

### Blockchain File Path
```bash
export BCHOC_FILE_PATH="chain.db"
```
If not set, `bchoc` defaults to `bchoc.db`.

---

## 🔧 Implemented Commands

### Command Summary

| Command | Description | Password Requirement |
|--------|-------------|----------------------|
| **init** | Create a new blockchain with a genesis block | None |
| **add** | Add evidence items (as CHECKEDIN) | Creator password |
| **checkout** | CHECKEDIN → CHECKEDOUT | Owner password |
| **checkin** | CHECKEDOUT → CHECKEDIN | Owner password |
| **remove** | Mark item as DISPOSED / DESTROYED / RELEASED | Creator password |
| **show cases** | List all case UUIDs | Optional owner password |
| **show items** | List item IDs for a case | Optional owner password |
| **show history** | Timeline of blocks (filterable) | Owner password |
| **verify** | Validate blockchain integrity | None |
| **summary** | Summary of item states for a case | Optional owner password |

---

## 📜 Command Details

### `init`
Creates the genesis (INITIAL) block.

```bash
./bchoc init
```

### `add`
Adds one or more items as **CHECKEDIN**.

```bash
./bchoc add \
  -c <case_uuid> \
  -i <item_id_1> [-i <item_id_2> ...] \
  -g <creator_name> \
  -p <creator_password>
```

### `checkout`
CHECKEDIN → CHECKEDOUT.

```bash
./bchoc checkout \
  -i <item_id> \
  -p <owner_password>
```

### `checkin`
CHECKEDOUT → CHECKEDIN.

```bash
./bchoc checkin \
  -i <item_id> \
  -p <owner_password>
```

### `remove`
Marks item as **DISPOSED**, **DESTROYED**, or **RELEASED** (must be CHECKEDIN).

```bash
./bchoc remove \
  -i <item_id> \
  -y DISPOSED|DESTROYED|RELEASED \
  [-o "Released To Name"] \
  -p <creator_password>
```

### `show cases`

```bash
./bchoc show cases
# or
./bchoc show cases -p <owner_password>
```

### `show items`

```bash
./bchoc show items \
  -c <case_uuid> \
  [-p <owner_password>]
```

### `show history`

```bash
./bchoc show history \
  -p <owner_password> \
  [-c <case_uuid>] \
  [-i <item_id>] \
  [-n N] \
  [-r]
```

### `verify`

```bash
./bchoc verify
```

### `summary`

```bash
./bchoc summary \
  -c <case_uuid> \
  [-p <owner_password>]
```

---

## 🧪 State Transition Rules

The verifier enforces:

- First appearance of an item **must** be CHECKEDIN  
- CHECKEDIN ↔ CHECKEDOUT must alternate properly  
- Removal types allowed **only** from CHECKEDIN  
- Hash chain must be fully correct  
- Genesis block must be INITIAL  

---

## 🛠 Build & Run Instructions

### 1️⃣ Install Python Dependencies

```bash
pip install -r packages
```

### 2️⃣ Make Executable

```bash
chmod +x bchoc
```

Or:

```bash
make
```

### 3️⃣ Set Required Environment Variables

```bash
export BCHOC_FILE_PATH="chain.db"

export BCHOC_PASSWORD_CREATOR="C67C"
export BCHOC_PASSWORD_POLICE="P80P"
export BCHOC_PASSWORD_LAWYER="L76L"
export BCHOC_PASSWORD_ANALYST="A65A"
export BCHOC_PASSWORD_EXECUTIVE="E69E"
```

---

## ▶️ Example Session

```bash
./bchoc init

./bchoc add \
  -c 0b711606-090e-40fb-8f9a-b82347a43887 \
  -i 3463648746 \
  -g 469teacher \
  -p C67C

./bchoc checkout -i 3463648746 -p P80P
./bchoc checkin  -i 3463648746 -p P80P

./bchoc show cases -p P80P
./bchoc show items -c 0b711606-090e-40fb-8f9a-b82347a43887 -p P80P

./bchoc show history -i 3463648746 -p P80P

./bchoc remove -i 3463648746 -y DISPOSED -p C67C

./bchoc verify

./bchoc summary -c 0b711606-090e-40fb-8f9a-b82347a43887 -p P80P
```

---

# 🤖 Generative AI Acknowledgment (Track 1 Requirement)

This project complies with the **CSE 469 Track 1 AI Usage Policy**.  
We used ChatGPT (OpenAI, 2024) **only as a coding assistant**, and all final code was:

- Reviewed manually  
- Tested extensively  
- Integrated and modified to match project rules and the autograder  

### Where AI Was Used

#### `block_helper.py`
We requested assistance designing:

- A fixed-size binary block header layout (`struct`)
- AES encryption/decryption helpers

**Prompt examples (documented as comments in the file):**

- *“Design a Python helper module that packs and unpacks a fixed-size binary block header using struct, with AES-encrypted case_id and item_id fields.”*

We then adapted these suggestions for CSE 469 specifications and added:

- INITIAL block rules  
- Decryption failover logic  
- Malformed field handling  

#### `bchoc` Main Script
We requested help with:

- argparse subcommand structure  
- Debugging state transitions  
- Timestamp formatting logic  

**Prompt examples inside the script:**

- *“Give me an argparse setup with subcommands: init, add, checkout, checkin, remove, show, verify, summary.”*  
- *“Help me debug a Python function that verifies a blockchain hash chain and item state transitions.”*

### In-Code Documentation
Every AI-assisted section contains comments in this format:

```python
# Generative AI Used: ChatGPT (OpenAI, 2024)
# Purpose: ...
# Prompt: "..."
```

### Reference
OpenAI. (2024). *ChatGPT* [Large language model]. https://openai.com/chatgpt

---

## 📄 End of README

