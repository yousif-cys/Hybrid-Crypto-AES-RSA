import struct
import os
from rsa_keys import rsa_encrypt, rsa_decrypt, load_public_key, load_private_key
from aes_cipher import generate_aes_key, aes_encrypt, aes_decrypt


def encrypt_file(input_path: str, output_path: str, public_key_path: str):
    """
    تشفير ملف كامل بالتشفير الهجين
    
    هيكل الملف المشفر:
    [4 بايت: طول مفتاح AES المشفر]
    [N بايت: مفتاح AES المشفر بـ RSA]
    [12 بايت: nonce]
    [16 بايت: authentication tag]
    [بقية: الملف المشفر بـ AES]
    """
    
    print(f"🔐 encrypting : {input_path}")
    
    # 1. قراءة الملف الأصلي
    with open(input_path, 'rb') as f:
        file_data = f.read()
    
    # 2. توليد مفتاح AES عشوائي جديد
    aes_key = generate_aes_key()
    
    # 3. تشفير محتوى الملف بـ AES
    nonce, ciphertext, tag = aes_encrypt(aes_key, file_data)
    
    # 4. تشفير مفتاح AES بـ RSA
    public_key = load_public_key(public_key_path)
    encrypted_aes_key = rsa_encrypt(public_key, aes_key)
    
    # 5. كتابة كل شيء في ملف واحد
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as f:
        # طول مفتاح AES المشفر (لنعرف كم بايت نقرأ عند فك التشفير)
        key_length = len(encrypted_aes_key)
        f.write(struct.pack('>I', key_length))   # 4 بايت big-endian
        
        # مفتاح AES المشفر
        f.write(encrypted_aes_key)
        
        # nonce و tag
        f.write(nonce)
        f.write(tag)
        
        # الملف المشفر
        f.write(ciphertext)
    
    print(f"✅ file decrypted:  {output_path}")
    print(f"   orginal size: {len(file_data):,} byte")
    print(f"   the new size: {os.path.getsize(output_path):,} byte")


def decrypt_file(input_path: str, output_path: str, private_key_path: str, password=None):
    
    print(f"🔓 decrypting {input_path}")
    
    with open(input_path, 'rb') as f:
        # 1. قراءة طول مفتاح AES المشفر
        key_length = struct.unpack('>I', f.read(4))[0]
        
        # 2. قراءة مفتاح AES المشفر
        encrypted_aes_key = f.read(key_length)
        
        # 3. قراءة nonce و tag
        nonce = f.read(12)
        tag   = f.read(16)
        
        # 4. قراءة باقي الملف المشفر
        ciphertext = f.read()
    
    # 5. فك تشفير مفتاح AES بـ RSA
    private_key = load_private_key(private_key_path, password)
    if private_key is None:
        print("❌ we cancel the process")
        return False
    aes_key = rsa_decrypt(private_key, encrypted_aes_key)
    
    # 6. فك تشفير الملف بـ AES
    plaintext = aes_decrypt(aes_key, nonce, ciphertext, tag)
    
    # 7. حفظ الملف الأصلي
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    print(f"✅ we decrypting the file: {output_path}")
    return True