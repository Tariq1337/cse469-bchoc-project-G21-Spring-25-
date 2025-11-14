CSE 469: Blockchain Chain of Custody (bchoc)
This is a Track 1 (Programming Language-Based) solution for the CSE 469 group project. It is a command-line program, bchoc, that implements a secure chain of custody log for forensic evidence using a custom, file-based blockchain.
The program is written in Python 3.
Group Member(s)
[YOUR NAME] (ASU ID: [YOUR ASU ID])
(Add other members here if you have them)
Program Description
This program implements all 10 required commands for managing and verifying the chain of custody:
init: Initializes a new blockchain file with a Genesis block.
add: Adds one or more new evidence items to a case (requires creator password).
checkout: Checks out an item, changing its state from CHECKEDIN to CHECKEDOUT (requires owner password).
checkin: Checks in an item, changing its state from CHECKEDOUT to CHECKEDIN (requires owner password).
remove: Removes an item from the chain (requires creator password and CHECKEDIN state).
show cases: Lists all unique case IDs in the blockchain.
show items: Lists all unique items for a given case ID.
show history: Shows the complete, chronologically-ordered transaction history for an item.
verify: Verifies the integrity of the entire blockchain by checking its hash chain.
summary: Provides a final count of items in each state for a given case.
How to Run
The program is designed to run in a Linux environment (e.g., Ubuntu 18.04+).
1. Build the Executable
First, use the Makefile to ensure the bchoc script is executable:
make


2. Set Environment Variables
The program reads all passwords from environment variables, as required by the project specification.
export BCHOC_PASSWORD_CREATOR="C67C"
export BCHOC_PASSWORD_POLICE="P80P"
export BCHOC_PASSWORD_ANALYST="A65A"
export BCHOC_PASSWORD_LAWYER="L76L"
export BCHOC_PASSWORD_EXECUTIVE="E69E"


3. Run the Program
The program must be told where to find or create the blockchain file using the BCHOC_FILE_PATH environment variable.
All commands are run using the ./bchoc executable.
# Example: Initialize the chain
BCHOC_FILE_PATH="chain.db" ./bchoc init

# Example: Add an item
BCHOC_FILE_PATH="chain.db" ./bchoc add -c "0b711606-090e-40fb-8f9a-b82347a43887" -i 3463648746 -g "creator1" -p "C67C"

# Example: Verify the chain
BCHOC_FILE_PATH="chain.db" ./bchoc verify

# Example: Show a summary
BCHOC_FILE_PATH="chain.db" ./bchoc summary -c "0b711606-090e-4_YOUR_ASU_ID43887" -p "P80P"


Generative AI Acknowledgment
Generative AI Acknowledgment: Portions of the code in this project were
generated with assistance from Gemini, a large language model trained by Google.
Reference: Google. (2024). Gemini [Large language model].
