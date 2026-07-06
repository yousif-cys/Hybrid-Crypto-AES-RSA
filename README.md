# 🔐 Hybrid Crypto System (AES + RSA)

A secure file storage system that leverages hybrid cryptography to encrypt and decrypt files safely.

## ⚙️ How It Works
- **AES-256-GCM:** Encrypts the file content with high performance and data integrity verification.
- **RSA-2048:** Encrypts the AES key securely for safe key distribution.
- **Password Protection:** Encrypts and protects your private key locally on your PC.

## 🚀 Features
- **Hybrid Cryptography:** Securely encrypt any file type using combined symmetric and asymmetric algorithms.
- **Asymmetric Decryption:** Decrypt files locally using your protected RSA private key.
- **Contact Management:** A built-in system to securely store and manage public keys of your contacts.
- **User-Friendly GUI:** Simple and clean graphical user interface.

## 🛠️ Technologies & Dependencies

*   **Language:** Python `3.8+`
*   **Cryptography:** `cryptography` library (AES-256-GCM, RSA-2048)
*   **GUI Framework:** `tkinter` (Built-in)

### Requirements
```bash
pip install cryptography
```

## 💻 How To Run
```bash
python GUI.py
```

## 📂 Project Structure
```text
.
├── GUI.py            # Graphical user interface
├── main.py           # Core application logic
├── rsa_keys.py       # RSA key generation and management
├── aes_cipher.py     # AES encryption and decryption functions
├── file_handler.py   # File I/O operations
└── contacts.py       # Contact and public key management
```
## Screenshots

### Main Menu
![Main Menu](screenshots/main-menu.png)

### Add Contact
![Error Add Key](screenshots/error-add-key.png)
![Key Name](screenshots/key-name.png)
![List Keys](screenshots/list-keys.png)

### Encrypt File
![Enter Key Name](screenshots/enter-key-name.png)
![File Encrypted Path](screenshots/file-encrypted-path.png)

### Decrypt File
![Enter Private Key Password](screenshots/enter-private-key-pass.png)
![Private Key Password](screenshots/private-key-pass.png)
![File Decrypted Path](screenshots/file-decrypted-path.png)
