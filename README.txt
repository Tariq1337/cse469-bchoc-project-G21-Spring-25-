CSE 469 – Blockchain Chain of Custody (bchoc)
Group 21 – Track 1 (Programming Language-Based)

Group Members
-------------
Tariq Bahaaaldeen – ASU ID: 1223918566  
Abhinav Ranish – ASU ID: 1226800395  
Raiden Ison – ASU ID: 1218779887  
Hansel Kunaseelan Nadar – ASU ID: 1224956915  
Ismail Wehelie – ASU ID: 1224733367  


Overview
--------
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
---------------------
The program reads and writes to a single blockchain file whose path is taken from the
BCHOC_FILE_PATH environment variable. If that variable is not set, the default file name
is bchoc.db in the current working directory.

The blockchain consists of a sequence of binary blocks. Each block contains:

- prev_hash (32 bytes)
- timestamp (double)
- encrypted case_id (32 bytes, hex-encoded AES)
- encrypted item_id (32 bytes, hex-encoded AES)
- state (12-byte string, e.g., INITIAL, CHECKEDIN, CHECKEDOUT, DISPOSED, DESTROYED, RELEASED)
- creator (12-byte string)
- owner (12-byte string)
- data_len (unsigned int) followed by data bytes

The helper module block_helper.py is responsible for:

- encrypting and decrypting case_id and item_id values
- packing logical fields into the binary block format
- unpacking binary blocks back into Python dictionaries

The main bchoc script:

- parses command-line arguments using argparse subparsers
- validates passwords using environment variables for the different roles
- derives current item state and metadata by scanning the blockchain (no separate database)
- appends new blocks for each command while preserving the hash chain


Commands and Passwords
----------------------
The following environment variables must be set before running the program:

- BCHOC_PASSWORD_CREATOR
- BCHOC_PASSWORD_POLICE
- BCHOC_PASSWORD_LAWYER
- BCHOC_PASSWORD_ANALYST
- BCHOC_PASSWORD_EXECUTIVE

In our testing we used the following example values:

export BCHOC_PASSWORD_CREATOR="C67C"  
export BCHOC_PASSWORD_POLICE="P80P"  
export BCHOC_PASSWORD_LAWYER="L76L"  
export BCHOC_PASSWORD_ANALYST="A65A"  
export BCHOC_PASSWORD_EXECUTIVE="E69E"

The "creator" password is used for creating evidence entries and removing items.
Any of the owner passwords (police, lawyer, analyst, executive) can act as an evidence
owner for check-out/check-in and for viewing history.

Supported commands:

1) init
   - Initializes the blockchain file with a single INITIAL (genesis) block if it does not
     already exist.
   - If the file already contains a valid blockchain, nothing is changed; if the file
     exists but is invalid or partially written, init exits with an error.

2) add
   - Adds one or more evidence items for a given case.
   - Each new item is recorded as a CHECKEDIN block.
   - Requires the creator password (BCHOC_PASSWORD_CREATOR).
   - Fails if an item with the same item_id already exists in the blockchain.

3) checkout
   - Changes an item state from CHECKEDIN to CHECKEDOUT.
   - Requires any valid owner role password (police, lawyer, analyst, or executive).
   - Only allowed if the current state of the item is exactly CHECKEDIN.

4) checkin
   - Changes an item state from CHECKEDOUT back to CHECKEDIN.
   - Requires any valid owner role password.
   - Only allowed if the current state of the item is exactly CHECKEDOUT.

5) remove
   - Permanently marks an item as DISPOSED, DESTROYED, or RELEASED.
   - Only allowed when the item is currently CHECKEDIN.
   - Requires the creator password.
   - For RELEASED, an optional owner name may be stored in the data field of the block.
   - Once an item is removed, further check-in/check-out operations on that item are
     considered invalid and will be caught by verify.

6) show cases
   - Lists all unique case IDs in the blockchain (excluding the INITIAL block).
   - An owner password is optional; if provided, it must be a valid owner role password.

7) show items
   - Lists all unique item IDs for a given case ID.
   - An owner password is optional; if provided, it must be a valid owner role password.

8) show history
   - Displays the history of blocks that match an optional case ID and/or item ID.
   - Includes the INITIAL block if it matches the filters.
   - Supports:
     - -n to limit the number of entries
     - -r to reverse the order
   - Requires an owner role password.

9) verify
   - Walks the entire blockchain and verifies:
     * hash-chain integrity (each block’s hash matches the next block’s prev_hash)
     * legal state transitions for each item (CHECKEDIN/CHECKEDOUT/removal rules)
   - On success, prints the number of transactions and that the blockchain is CLEAN.
   - On failure, prints an ERROR state and identifies the bad block hash.

10) summary
    - For a given case ID, counts how many unique items end up in each final state:
      CHECKEDIN, CHECKEDOUT, DISPOSED, DESTROYED, RELEASED.
    - Prints a brief summary report including total evidence items for that case.
    - An owner password is optional; if provided, it must be a valid owner role password.


Building and Running
--------------------
This project targets Python 3 on Linux (Ubuntu recommended).

1) Install required Python packages:

   pip install -r packages

   (packages currently includes pycryptodome and dos2unix.)

2) Make the bchoc script executable (if needed):

   chmod +x bchoc

3) Set the necessary environment variables, for example:

   export BCHOC_FILE_PATH="chain.db"
   export BCHOC_PASSWORD_CREATOR="C67C"
   export BCHOC_PASSWORD_POLICE="P80P"
   export BCHOC_PASSWORD_LAWYER="L76L"
   export BCHOC_PASSWORD_ANALYST="A65A"
   export BCHOC_PASSWORD_EXECUTIVE="E69E"

   If BCHOC_FILE_PATH is not set, the program uses the default file name bchoc.db.

4) Run commands such as:

   ./bchoc init

   ./bchoc add -c <case_uuid> -i <item_id> -g <creator_name> -p <creator_password>

   ./bchoc checkout -i <item_id> -p <owner_password>

   ./bchoc checkin -i <item_id> -p <owner_password>

   ./bchoc remove -i <item_id> -y DISPOSED -p <creator_password>

   ./bchoc show cases -p <owner_password>

   ./bchoc show items -c <case_uuid> -p <owner_password>

   ./bchoc show history -p <owner_password> [-c <case_uuid>] [-i <item_id>] [-n N] [-r]

   ./bchoc verify

   ./bchoc summary -c <case_uuid> -p <owner_password>


Generative AI Acknowledgment
----------------------------
This is a Track 1 project. We used generative AI (ChatGPT by OpenAI) as a coding assistant
for some limited parts of the implementation and for debugging guidance. The final code
was reviewed, tested, and integrated by the team.

In particular:

- In block_helper.py we asked ChatGPT for help designing the binary block layout and
  AES-based helper functions. We then customized the code to match the project specification
  and fixed edge cases (such as handling the INITIAL block and invalid encrypted IDs).

- In bchoc (the main script) we used ChatGPT to suggest an argparse subcommand skeleton and
  to help debug some tricky state-transition and timestamp formatting issues. We then
  adapted the structure, added all project-specific logic, and corrected behavior based
  on the course autograder results.

Within the source files bchoc and block_helper.py there are code comments that explicitly
mark where generative AI assistance was used, describe the purpose of the assistance,
and include the original prompts we provided.

Reference:
OpenAI. (2024). ChatGPT [Large language model]. https://openai.com/chatgpt
