# CSE 469 Group Project - Group 21
# Members: Tariq Bahaaaldeen, Abhinav Ranish, Raiden Ison, Hansel Kunaseelan Nadar, Ismail Wehelie
# Description: Helper functions for packing/unpacking binary blocks and handling encryption.

import struct
import uuid
from Crypto.Cipher import AES

# AES key hardcoded from project specification
AES_KEY = b"R0chLi4uLi4uLi4="

# Block header format: 32s (prev_hash), d (timestamp), 32s (case_id), 32s (item_id),
# 12s (state), 12s (creator), 12s (owner), I (data_len)
BLOCK_HEADER_FORMAT = "32s d 32s 32s 12s 12s 12s I"
BLOCK_HEADER_SIZE = struct.calcsize(BLOCK_HEADER_FORMAT)


# Generative AI Used: ChatGPT (OpenAI, November 15, 2025)
# Purpose: Get help drafting the basic AES-ECB encrypt/decrypt helper structure,
#          including padding strategy and general function skeletons for this project.
# Prompt: "For a CSE 469 blockchain chain-of-custody project, write simple Python helper
#          functions encrypt_data and decrypt_data using AES-ECB with a fixed key and
#          16-byte block padding. They should work on arbitrary byte strings."
def encrypt_data(data):
    """
    Encrypt a byte string using AES-ECB with the project-specified key.
    """
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_data = data.rjust(16, b'\0')
    return cipher.encrypt(padded_data)


def decrypt_data(ciphertext):
    """
    Decrypt a byte string using AES-ECB and remove leading null padding.
    """
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_data = cipher.decrypt(ciphertext)
    return padded_data.lstrip(b'\0')


# Generative AI Used: ChatGPT (OpenAI, November 15, 2025)
# Purpose: Help design the struct packing layout and function skeleton for turning a
#          logical block (prev_hash, timestamp, case_id, item_id, state, creator, owner,
#          data) into a binary representation that matches the project spec.
# Prompt: "Given a block header format '32s d 32s 32s 12s 12s 12s I' for a blockchain
#          project, write a Python function pack_block(...) that encrypts a UUID case_id
#          and integer item_id with AES, stores them as hex-encoded bytes, pads state,
#          creator, owner to 12 bytes, and appends the raw data after the header."
def pack_block(prev_hash, timestamp, case_id_str, item_id_int, state, creator, owner, data=b""):
    """
    Pack a single blockchain block into its binary representation.
    """
    case_id_bytes = uuid.UUID(case_id_str).bytes
    encrypted_case = encrypt_data(case_id_bytes)
    enc_case_id = encrypted_case.hex().encode('utf-8')
    
    item_id_bytes = item_id_int.to_bytes(4, 'big')
    encrypted_item = encrypt_data(item_id_bytes)
    enc_item_id = encrypted_item.hex().encode('utf-8')
    
    state_bytes = state.encode('utf-8').ljust(12, b'\0')
    creator_bytes = creator.encode('utf-8').ljust(12, b'\0')
    owner_bytes = owner.encode('utf-8').ljust(12, b'\0')
    
    header = struct.pack(
        BLOCK_HEADER_FORMAT,
        prev_hash,
        timestamp,
        enc_case_id,
        enc_item_id,
        state_bytes,
        creator_bytes,
        owner_bytes,
        len(data)
    )
    
    return header + data


# Generative AI Used: ChatGPT (OpenAI, November 15, 2025)
# Purpose: Get assistance with the logic for unpacking a binary block, particularly:
#          (1) handling the INITIAL (genesis) block without decrypting invalid IDs,
#          (2) safely decoding encrypted case_id/item_id back to usable values, and
#          (3) deciding how to fall back on ValueError when corrupted data is seen.
# Prompt: "Help me write a Python function unpack_block(block_bytes) for my CSE 469
#          blockchain project that reverses pack_block: it should unpack the header
#          using the same struct format, decrypt the hex-encoded AES case_id and
#          item_id, treat state == 'INITIAL' as a special genesis block with zero
#          IDs, and return a dictionary with prev_hash, timestamp, case_id, item_id,
#          state, creator, owner, data_len, and data."
def unpack_block(block_bytes):
    """
    Unpack a single binary block into its Python dictionary representation.
    Handles the special INITIAL (genesis) block without attempting decryption.
    """
    header_bytes = block_bytes[:BLOCK_HEADER_SIZE]
    data_bytes = block_bytes[BLOCK_HEADER_SIZE:]
    
    (
        prev_hash,
        timestamp,
        enc_case_id,
        enc_item_id,
        state_bytes,
        creator_bytes,
        owner_bytes,
        data_len
    ) = struct.unpack(BLOCK_HEADER_FORMAT, header_bytes)

    state = state_bytes.decode('utf-8').rstrip('\0')
    creator = creator_bytes.decode('utf-8').rstrip('\0')
    owner = owner_bytes.decode('utf-8').rstrip('\0')

    if state == "INITIAL":
        # Genesis block: no valid encrypted case/item IDs to decode.
        case_id_str = "00000000-0000-0000-0000-000000000000"
        item_id_int = 0
    else:
        try:
            enc_case_bytes = bytes.fromhex(enc_case_id.decode('utf-8'))
            dec_case_id_bytes = decrypt_data(enc_case_bytes)
            case_id_str = str(uuid.UUID(bytes=dec_case_id_bytes))
            
            enc_item_bytes = bytes.fromhex(enc_item_id.decode('utf-8'))
            dec_item_id_bytes = decrypt_data(enc_item_bytes)
            item_id_int = int.from_bytes(dec_item_id_bytes, 'big')
        except ValueError:
            # On any decoding failure, fall back to zero identifiers.
            case_id_str = "00000000-0000-0000-0000-000000000000"
            item_id_int = 0
    
    return {
        "prev_hash": prev_hash,
        "timestamp": timestamp,
        "case_id": case_id_str,
        "item_id": item_id_int,
        "state": state,
        "creator": creator,
        "owner": owner,
        "data_len": data_len,
        "data": data_bytes[:data_len]
    }
