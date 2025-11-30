import base64
import json
import os
from bson import ObjectId
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Load Key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "my_super_secret_key_32_chars_long!")
# Ensure key is bytes
KEY_BYTES = ENCRYPTION_KEY.encode('utf-8')[:32] 

# Custom Encoder for MongoDB ObjectId and Datetime
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def encrypt_payload(data):
    try:
        # 1. Convert Data to JSON String
        json_data = json.dumps(data, cls=MongoJSONEncoder)
        data_bytes = json_data.encode('utf-8')

        # 2. Generate Random IV (16 bytes)
        iv = os.urandom(16)

        # 3. Pad Data (AES block size is 128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data_bytes) + padder.finalize()

        # 4. Encrypt using AES-256-CBC
        cipher = Cipher(algorithms.AES(KEY_BYTES), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # 5. Combine IV + Ciphertext -> Base64 Encode
        # We prepend the IV so the frontend knows how to decrypt
        combined = iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')

    except Exception as e:
        print(f"Encryption Error: {e}")
        return None