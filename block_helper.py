# CSE 469 Group Project - Group 21
# Members: Tariq Bahaaaldeen, Abhinav Ranish, Raiden Ison, Hansel Kunaseelan Nadar
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

def encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_data = data.rjust(16, b'\0')
    return cipher.encrypt(padded_data)

def decrypt_data(ciphertext):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_data = cipher.decrypt(ciphertext)
    return padded_data.lstrip(b'\0')

def pack_block(prev_hash, timestamp, case_id_str, item_id_int, state, creator, owner, data=b""):
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

def unpack_block(block_bytes):
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
