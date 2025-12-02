CSE 469 – Blockchain Chain of Custody (bchoc)
Group 21 – Track 1 (Programming Language-Based)

Group Members

Tariq Bahaaaldeen – ASU ID: 1223918566
Abhinav Ranish – ASU ID: 1226800395
Raiden Ison – ASU ID: 1218779887
Hansel Kunaseelan Nadar – ASU ID: 1224956915
Ismail Wehelie – ASU ID: 1224733367

Overview

This project implements bchoc, a command-line tool that maintains a secure, tamper-evident
digital chain of custody for forensic evidence. The tool is written in Python 3 and uses a
single binary blockchain file to record all evidence-related actions.

Each operation on an evidence item (adding, checking out, checking in, removing, etc.) is
recorded as a new block appended to the blockchain file. No blocks are modified in place.
The hash of each block is used as the prev_hash for the next block, so any change to past
data can be detected by re-verifying the hash chain.

Case IDs (UUIDs) and item IDs (integers) are encrypted using AES in ECB mode before being
stored in the blockchain. This prevents casual inspection of IDs directly from the file.

How the Program Works

The program reads and writes to a single blockchain file whose path is taken from the
BCHOC_FILE_PATH environment variable. If that variable is not set, the default file name
is bchoc.db.

The blockchain consists of a sequence of binary blocks. Each block contains:

prev_hash (32 bytes)

timestamp (double)

encrypted case_id (32 bytes, hex-encoded AES)

encrypted item_id (32 bytes, hex-encoded AES)

state (12-byte string, e.g., INITIAL, CHECKEDIN, CHECKEDOUT, DISPOSED, DESTROYED, RELEASED)

creator (12-byte string)

owner (12-byte string)

data_len (unsigned int) followed by data bytes

The helper module block_helper.py is responsible for:

encrypting and decrypting case_id and item_id values

packing logical fields into the binary block format

unpacking binary blocks back into Python dictionaries

The main bchoc script:

parses command-line arguments using argparse subparsers

validates passwords using environment variables for the different roles

derives current item state and metadata by scanning the blockchain (no separate database)

appends new blocks for each command while preserving the hash chain

Commands and Passwords

The following environment variables must be set before running the program:

BCHOC_PASSWORD_CREATOR

BCHOC_PASSWORD_POLICE

BCHOC_PASSWORD_LAWYER

BCHOC_PASSWORD_ANALYST

BCHOC_PASSWORD_EXECUTIVE

The "creator" password is used for creating evidence entries and removing items.
Any of the owner passwords (police, lawyer, analyst, executive) can act as an evidence owner.

Supported commands:

init

Initializes the blockchain file with a single INITIAL (genesis) block if it does not
already exist. If the file already contains a valid blockchain, nothing is changed.

add

Adds one or more evidence items for a given case.

Each new item is recorded as a CHECKEDIN block.

Requires the creator password.

checkout

Changes an item state from CHECKEDIN to CHECKEDOUT.

Requires an owner role password.

checkin

Changes an item state from CHECKEDOUT back to CHECKEDIN.

Requires an owner role password.

remove

Permanently marks an item as DISPOSED, DESTROYED, or RELEASED.

Only allowed when the item is currently CHECKEDIN.

Requires the creator password.

For RELEASED, an optional owner name may be stored in the data field.

show cases

Lists all unique case IDs in the blockchain (excluding the INITIAL block).

An owner password is optional; if provided, it must be valid.

show items

Lists all unique item IDs for a given case ID.

An owner password is optional; if provided, it must be valid.

show history

Displays the full history of blocks that match an optional case ID and/or item ID.

Supports:
-n to limit the number of entries
-r to reverse the order

Requires an owner role password.

verify

Walks the entire blockchain and verifies:

hash-chain integrity (each block’s hash matches the next block’s prev_hash)

legal state transitions for each item (CHECKEDIN/CHECKEDOUT/removal rules)

Prints whether the blockchain is CLEAN or ERROR.

summary

For a given case ID, counts how many unique items end up in each final state:
CHECKEDIN, CHECKEDOUT, DISPOSED, DESTROYED, RELEASED.

Prints a brief summary report.

An owner password is optional; if provided, it must be valid.

Building and Running

This project targets Python 3 on Linux (Ubuntu recommended).

Install required Python packages:

pip install -r packages

Make the bchoc script executable (if needed):

chmod +x bchoc

Set the necessary environment variables, for example:

export BCHOC_FILE_PATH="chain.db"
export BCHOC_PASSWORD_CREATOR="C67C"
export BCHOC_PASSWORD_POLICE="P8BP"
export BCHOC_PASSWORD_LAWYER="I76L"
export BCHOC_PASSWORD_ANALYST="A6SA"
export BCHOC_PASSWORD_EXECUTIVE="E69E"

Run commands such as:

./bchoc init
./bchoc add -c <case_uuid> -i <item_id> -g <creator_name> -p <creator_password>
./bchoc checkout -i <item_id> -p <owner_password>
./bchoc checkin -i <item_id> -p <owner_password>
./bchoc remove -i <item_id> -y DISPOSED -p <creator_password>
./bchoc show cases
./bchoc show items -c <case_uuid>
./bchoc show history -p <owner_password> [-c <case_uuid>] [-i <item_id>] [-n N] [-r]
./bchoc verify
./bchoc summary -c <case_uuid>

Generative AI Acknowledgment

Portions of the code in this project were generated with assistance from ChatGPT, an AI tool
developed by OpenAI. Code comments in bchoc and block_helper.py identify where generative
AI was used, describe the purpose of the assistance, and include the original prompts.

Reference:
OpenAI. (2024). ChatGPT [Large language model].
openai.com/chatgpt
