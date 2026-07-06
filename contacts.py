import json
import os

def load_contacts():
    if not os.path.exists("contacts.json"):
        return {}
    else:
        with open("contacts.json", 'r') as f:
            content = f.read()
            if content == "":
                return {}
            return json.loads(content)
        
def save_contacts(name,public_key_path):
    contact = load_contacts()
    contact[name] = public_key_path

    with open("contacts.json",'w') as f:
        json.dump(contact, f, ensure_ascii=False, indent=4)

def list_contacts():
    contacts = load_contacts()
    if not contacts:
        print("THE FILE IS EMPTY")
    else:
        for name, path in contacts.items():
            print(f"{name} : {path}")