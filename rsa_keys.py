from tkinter import messagebox, simpledialog
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    return private_key,public_key
def save_private_key(private_key, filepath, password=None):
    if password:
        encryption = serialization.BestAvailableEncryption(password.encode())
    else:
        encryption = serialization.NoEncryption()
    pem_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
    )
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(pem_data)   
        print(f"✅ we save the private key: {filepath}")     
def save_public_key(public_key, filepath):
    
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(pem_data)
    print(f"✅ we save the public key: {filepath}")

def load_private_key(filepath, password):
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    
    while True:
        pwd = password.encode() if password else None
        
        try:
            return serialization.load_pem_private_key(pem_data, password=pwd)
        
        except Exception:
            password = simpledialog.askstring(
                "❌ the password is INCORRECT : ",
            
                "ENTER THE PASSWORD again or Click 'Cancel' to cancel the process : ",
                show='*'
            )
            if password is None:
                messagebox.showinfo("❌ Canceling","the process has been canceled")
                return None
        
def load_public_key(filepath):
    
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    
    return serialization.load_pem_public_key(pem_data)

def rsa_encrypt(public_key, data: bytes) -> bytes:
    
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt(private_key, encrypted_data: bytes) -> bytes:
    
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
