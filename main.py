import os
from rsa_keys import generate_rsa_keys, save_private_key, save_public_key
from file_handler import encrypt_file, decrypt_file
from contacts import load_contacts, save_contacts, list_contacts


def setup_keys():
    from tkinter import simpledialog, Tk
    
    private_key_path = "keys/private_key.pem"
    public_key_path  = "keys/public_key.pem"
    
    if not os.path.exists(private_key_path):
        root = Tk()
        root.withdraw()  # إخفاء النافذة الفارغة
        
        input_key = simpledialog.askstring(
            "كلمة المرور",
            "أدخل كلمة مرور للمفتاح الخاص أو اضغط Cancel:",
            show='*'
        )
        root.destroy()
        
        private_key, public_key = generate_rsa_keys()
        save_private_key(private_key, private_key_path, input_key)
        save_public_key(public_key, public_key_path)
    
    return private_key_path, public_key_path


def main():
    print("=" * 50)
    print(" system of encrypted files - AES + RSA")
    print("=" * 50)
    
    private_key_path, public_key_path = setup_keys()
    
    while True:
        print("\n📋 choose")
        print("  1. encrypt file")
        print("  2. decrypt file")
        print("  3. add contact")
        print("  4. list contacts")
        print("  5. Exit")
        
        choice = input("choose number: ").strip()
        
        if choice == "1":
            while True:
                input_file = input("enter the path of the file: ").strip()
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
            output_file = input("the path to save the encrypted file or (Enter to defualt): ").strip()
            if not output_file:
                filename = os.path.basename(input_file)
                output_file = f"encrypted/{filename}.enc"
        
            encrypt_file(input_file, output_file, public_key_path)
        
        elif choice == "2":
            while True:
                input_file  = input("path of the file you want to Encrypt ").strip()
                if input_file == "":
                        print("❌ You hit Enter by mistake, please enter the file path")
                elif not os.path.exists(input_file):
                        print("❌ File not found, please check the path")    
                else:
                    break
            input_key = input("Enter the key : ").strip()

            output_file = input("the path to save the decrypted file or (Enter to defualt): ").strip()
            
            if not output_file:
                filename = os.path.basename(input_file).replace('.enc', '')
                output_file = f"decrypted/{filename}"
            
            decrypt_file(input_file, output_file, private_key_path, input_key)
        
        elif choice == "3":
            name = input("give me the name of contact : ")
            public_key_path= input("give me the path for public key: ").strip()
            while True:
                public_key_path = input("give me the path for public key: ").strip()
                if public_key_path == "":
                    print("❌ You hit Enter by mistake, please enter the file path for public key : ")
                elif not os.path.exists(public_key_path):
                    print("❌ File not found, please check the path")    
                else:
                    break
            save_contacts(name,public_key_path)
        
        elif choice == "4":
            list_contacts()

        elif choice == "5":
            print("bye")
            break    
        else:
            print("❌ false choose :")


if __name__ == "__main__":
    main()