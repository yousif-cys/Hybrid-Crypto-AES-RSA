from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
import os

def generate_aes_key() -> bytes:
    return os.urandom(32)

def aes_encrypt(key=bytes , plaintext=bytes) -> tuple:
    nonce = os.urandom(12)
    cipher=Cipher(
        algorithms.AES(key),
        modes.GCM(nonce)
    )
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag
    return nonce,ciphertext,tag

def aes_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes) -> bytes:
    cipher=Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag)
    )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext
