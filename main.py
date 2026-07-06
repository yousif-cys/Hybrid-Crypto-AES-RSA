import os
from rsa_keys import generate_rsa_keys, save_private_key, save_public_key
from file_handler import encrypt_file, decrypt_file
from contacts import load_contacts, save_contacts, list_contacts


def setup_keys():
    from tkinter import simpledialog, Tk

    private_key_path = "keys/private_key.pem"
    public_key_path = "keys/public_key.pem"

    if not os.path.exists(private_key_path):
        root = Tk()
        root.withdraw()  # Hide the empty window

        input_key = simpledialog.askstring(
            "PASSWORD",
            "Enter password to secure the private key file: ",
            show='*'
        )
        root.destroy()

        private_key, public_key = generate_rsa_keys()
        save_private_key(private_key, private_key_path, input_key)
        save_public_key(public_key, public_key_path)

    return private_key_path, public_key_path


def main():
    print("=" * 50)
    print("System of encrypted files - AES + RSA")
    print("=" * 50)

    private_key_path, public_key_path = setup_keys()

    while True:
        print("\n📋 Choose")
        print("  1. Encrypt file")
        print("  2. Decrypt file")
        print("  3. Add contact")
        print("  4. List contacts")
        print("  5. Exit")

        choice = input("Choose a number: ").strip()

        if choice == "1":
            while True:
                input_file = input("Enter the path of the file: ").strip()
                if input_file == "":
                    print("❌ You hit Enter by mistake, please enter the file path")
                elif not os.path.exists(input_file):
                    print("❌ File not found, please check the path")
                else:
                    break
            while True:
                name = input("Enter contact name to encrypt for: ").strip()
                if name == "":
                    print("❌ You hit Enter by mistake, please enter the contact name")
                else:
                    contacts = load_contacts()
                    if name in contacts:
                        public_key_path = contacts[name]
                        break
                    else:
                        print("❌ Contact not found, please try again")
            output_file = input("Enter the path to save the encrypted file or press Enter for default: ").strip()
            if not output_file:
                filename = os.path.basename(input_file)
                output_file = f"encrypted/{filename}.enc"

            encrypt_file(input_file, output_file, public_key_path)

        elif choice == "2":
            while True:
                input_file = input("Enter the path of the file you want to decrypt: ").strip()
                if input_file == "":
                    print("❌ You hit Enter by mistake, please enter the file path")
                elif not os.path.exists(input_file):
                    print("❌ File not found, please check the path")
                else:
                    break
            input_key = input("Enter the key: ").strip()

            output_file = input("Enter the path to save the decrypted file or press Enter for default: ").strip()

            if not output_file:
                filename = os.path.basename(input_file).replace('.enc', '')
                output_file = f"decrypted/{filename}"

            decrypt_file(input_file, output_file, private_key_path, input_key)

        elif choice == "3":
            name = input("Enter the name of the contact: ")
            public_key_path = input("Enter the path for the public key: ").strip()
            while True:
                public_key_path = input("Enter the path for the public key: ").strip()
                if public_key_path == "":
                    print("❌ You hit Enter by mistake, please enter the file path for the public key")
                elif not os.path.exists(public_key_path):
                    print("❌ File not found, please check the path")
                else:
                    break
            save_contacts(name, public_key_path)

        elif choice == "4":
            list_contacts()

        elif choice == "5":
            print("Goodbye")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()