import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from unittest import result
from file_handler import encrypt_file, decrypt_file
from contacts import save_contacts, list_contacts, load_contacts
from rsa_keys import generate_rsa_keys, save_private_key, save_public_key
from main import setup_keys
import os


private_key_path, public_key_path = setup_keys()


def prompt_large_input(parent, title, prompt):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("420x180")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    tk.Label(dialog, text=prompt, font=("Arial", 11), wraplength=360).pack(padx=20, pady=(20, 10))

    entry = tk.Entry(dialog, width=35, font=("Arial", 11))
    entry.pack(padx=20, pady=10)
    entry.focus_set()

    result = {"value": None}

    def submit():
        result["value"] = entry.get()
        dialog.destroy()

    def cancel():
        dialog.destroy()

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=15)
    tk.Button(button_frame, text="OK", width=10, command=submit).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", width=10, command=cancel).pack(side="left", padx=10)

    dialog.wait_window(dialog)
    return result["value"]


def encrypt_action():
    # Select the file
    input_file = filedialog.askopenfilename(title="Select the file to encrypt")
    if not input_file:
        return

    # Select the recipient's public key
    contacts = load_contacts()
    if not contacts:
        messagebox.showerror("ERROR", "ADD KEY FIRST")
        return

    while True:
        names = list(contacts.keys())
        name = simpledialog.askstring("Key Name", f"Enter the key name:\n{', '.join(names)}")
        
        if name is None:  
            return
        elif name in contacts:
            selected_public_key = contacts[name]
            break
        else:
            messagebox.showerror("❌ Error", f"'{name}' not found, please enter the correct name")

    # Save path
    filename = os.path.basename(input_file)
    output_file = f"encrypted/{filename}.enc"

    encrypt_file(input_file, output_file, selected_public_key)
    messagebox.showinfo("Success", f"File encrypted!\nSaved to: {output_file}")


def decrypt_action():
    input_file = filedialog.askopenfilename(title="Select the encrypted file")
    if not input_file:
        return

    password = simpledialog.askstring("Password", "Enter the password to decrypt the file:", show='*')

    filename = os.path.basename(input_file).replace('.enc', '')
    output_file = f"decrypted/{filename}"

    result = decrypt_file(input_file, output_file, private_key_path, password)
    if result:
        messagebox.showinfo("✅ Success", f"File decrypted!\nSaved to: {output_file}")


def add_contact_action():
    name = prompt_large_input(window, "Add public key", "Enter the name of the key:")
    if not name:
        return

    key_path = filedialog.askopenfilename(title="Choose the public key file")
    if not key_path:
        return

    save_contacts(name, key_path)
    messagebox.showinfo("Success", f"{name} added successfully!")


def list_contacts_action():
    contacts = load_contacts()
    if not contacts:
        messagebox.showinfo("Saved Keys", "No saved keys found")
        return

    text = "\n".join([f"👤 {name}: {path}" for name, path in contacts.items()])
    messagebox.showinfo("Saved Keys", text)

# Create the main window
window = tk.Tk()
window.title("Secure File Storage")
window.geometry("400x500")
window.resizable(False, False)

# Title
title = tk.Label(
    window,
    text="🔐 Secure File Storage",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

subtitle = tk.Label(
    window,
    text="(AES + RSA Hybrid Encryption)",
    font=("Arial", 10)
)
subtitle.pack()

# Button frame
frame = tk.Frame(window)
frame.pack(pady=30)

# Encrypt button
btn_encrypt = tk.Button(
    frame,
    text="🔐 Encrypt File",
    font=("Arial", 12),
    width=25,
    height=2,
    bg="#2196F3",
    fg="white",
    command=encrypt_action
)
btn_encrypt.pack(pady=10)

# Decrypt button
btn_decrypt = tk.Button(
    frame,
    text="🔓 Decrypt File",
    font=("Arial", 12),
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white",
    command=decrypt_action
)
btn_decrypt.pack(pady=10)

# Add recipient key button
btn_add = tk.Button(
    frame,
    text="👤 Add Keys",
    font=("Arial", 12),
    width=25,
    height=2,
    bg="#FF9800",
    fg="white",
    command=add_contact_action
)
btn_add.pack(pady=10)

# List keys button
btn_list = tk.Button(
    frame,
    text="📋 List available Keys",
    font=("Arial", 12),
    width=25,
    height=2,
    bg="#9C27B0",
    fg="white",
    command=list_contacts_action
)
btn_list.pack(pady=10)
window.mainloop()
