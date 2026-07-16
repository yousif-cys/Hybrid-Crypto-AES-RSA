import struct
import os
from rsa_keys import rsa_encrypt, rsa_decrypt, load_public_key, load_private_key
from aes_cipher import generate_aes_key, aes_encrypt, aes_decrypt


def encrypt_file(input_path: str, output_path: str, public_key_path: str):
    
    print(f"🔐 encrypting : {input_path}")
    

    with open(input_path, 'rb') as f:
        file_data = f.read()
    

    aes_key = generate_aes_key()
    

    nonce, ciphertext, tag = aes_encrypt(aes_key, file_data)
    

    public_key = load_public_key(public_key_path)
    encrypted_aes_key = rsa_encrypt(public_key, aes_key)
    

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as f:

        key_length = len(encrypted_aes_key)
        f.write(struct.pack('>I', key_length))
        

        f.write(encrypted_aes_key)
        
        # nonce و tag
        f.write(nonce)
        f.write(tag)
        

        f.write(ciphertext)
    
    print(f"✅ file decrypted:  {output_path}")
    print(f"   orginal size: {len(file_data):,} byte")
    print(f"   the new size: {os.path.getsize(output_path):,} byte")


def decrypt_file(input_path: str, output_path: str, private_key_path: str, password=None):
    
    print(f"🔓 decrypting {input_path}")
    
    with open(input_path, 'rb') as f:

        key_length = struct.unpack('>I', f.read(4))[0]
        

        encrypted_aes_key = f.read(key_length)
        

        nonce = f.read(12)
        tag   = f.read(16)
        

        ciphertext = f.read()
    

    private_key = load_private_key(private_key_path, password)
    if private_key is None:
        print("❌ we cancel the process")
        return False
    aes_key = rsa_decrypt(private_key, encrypted_aes_key)
    

    plaintext = aes_decrypt(aes_key, nonce, ciphertext, tag)
    

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    print(f"✅ we decrypting the file: {output_path}")
    return True
