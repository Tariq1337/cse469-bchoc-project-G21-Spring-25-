import struct
import uuid
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Hardcoded AES key from the project spec
AES_KEY = b"R0chLi4uLi4uLi4="

# The block header structure format string
BLOCK_HEADER_FORMAT = "32s d 32s 32s 12s 12s 12s I"
BLOCK_HEADER_SIZE = struct.calcsize(BLOCK_HEADER_FORMAT)

# --- Encryption Functions ---

def encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_data = data.ljust(32, b'\0') 
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def decrypt_data(ciphertext):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_data = cipher.decrypt(ciphertext)
    data = padded_data.rstrip(b'\0')
    return data

# --- Block Packing/Unpacking Functions ---

def pack_block(prev_hash, timestamp, case_id_str, item_id_int, state, creator, owner, data=b""):
    case_id_bytes = uuid.UUID(case_id_str).bytes
    enc_case_id = encrypt_data(case_id_bytes)
    
    item_id_bytes = item_id_int.to_bytes(4, 'little')
    enc_item_id = encrypt_data(item_id_bytes)
    
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
    """
    Takes a single block's raw bytes, unpacks the header,
    decrypts sensitive fields, and returns a readable dictionary.
    """
    # 1. Separate header and data
    header_bytes = block_bytes[:BLOCK_HEADER_SIZE]
    data_bytes = block_bytes[BLOCK_HEADER_SIZE:]
    
    # 2. Unpack the header
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

    # 3. Decode state *first* to check for Genesis
    state = state_bytes.decode('utf-8').rstrip('\0')

    # 4. Handle Genesis block vs. Normal block
    if state == "INITIAL":
        # Genesis block has special non-encrypted, non-UUID/int fields
        case_id_str = "00000000-0000-0000-0000-000000000000"
        item_id_int = 0
    else:
        # Decrypt/Convert Case ID
        dec_case_id_bytes = decrypt_data(enc_case_id)
        case_id_str = str(uuid.UUID(bytes=dec_case_id_bytes))
        
        # Decrypt/Convert Item ID
        dec_item_id_bytes = decrypt_data(enc_item_id)
        item_id_int = int.from_bytes(dec_item_id_bytes, 'little')
    
    # 5. Decode other strings
    creator = creator_bytes.decode('utf-8').rstrip('\0')
    owner = owner_bytes.decode('utf-8').rstrip('\0')
    
    # 6. Return a nice dictionary
    return {
        "prev_hash": prev_hash,
        "timestamp": timestamp,
        "case_id": case_id_str,
        "item_id": item_id_int,
        "state": state,
        "creator": creator,
        "owner": owner,
        "data_len": data_len,
        "data": data_bytes[:data_len] # Only return the data specified by data_len
    }
