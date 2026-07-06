import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from file_handler import encrypt_file, decrypt_file
from contacts import save_contacts, list_contacts, load_contacts
from rsa_keys import generate_rsa_keys, save_private_key, save_public_key
from main import setup_keys
import os



private_key_path, public_key_path = setup_keys()

def encrypt_action():
    # اختيار الملف
    input_file = filedialog.askopenfilename(title="اختر الملف للتشفير")
    if not input_file:
        return
    
    # اختيار جهة الاتصال
    contacts = load_contacts()
    if not contacts:
        messagebox.showerror("خطأ", " أضف  أولاً المفتاح")
        return
    
    names = list(contacts.keys())
    name = simpledialog.askstring("اسم المفتاح ", f"أدخل اسم المفتاح :\n{', '.join(names)}")
    if not name or name not in contacts:
        messagebox.showerror("خطأ", "غير موجودة")
        return
    
    selected_public_key = contacts[name]
    
    # مسار الحفظ
    filename = os.path.basename(input_file)
    output_file = f"encrypted/{filename}.enc"
    
    encrypt_file(input_file, output_file, selected_public_key)
    messagebox.showinfo("✅ نجاح", f"تم تشفير الملف!\nمحفوظ في: {output_file}")


def decrypt_action():
    input_file = filedialog.askopenfilename(title="اختر الملف المشفر")
    if not input_file:
        return
    
    password = simpledialog.askstring("كلمة المرور", "أدخل كلمة المرور أو اتركها فارغة:", show='*')
    
    filename = os.path.basename(input_file).replace('.enc', '')
    output_file = f"decrypted/{filename}"
    
    decrypt_file(input_file, output_file, private_key_path, password)
    messagebox.showinfo("✅ نجاح", f"تم فك التشفير!\nمحفوظ في: {output_file}")


def add_contact_action():
    name = simpledialog.askstring("إضافة مفتاح عام", "أدخل الاسم:")
    if not name:
        return
    
    key_path = filedialog.askopenfilename(title="اختر ملف المفتاح العام")
    if not key_path:
        return
    
    save_contacts(name, key_path)
    messagebox.showinfo("✅ نجاح", f"تم إضافة {name} بنجاح!")


def list_contacts_action():
    contacts = load_contacts()
    if not contacts:
        messagebox.showinfo(" اسماء المفاتيح", "لا يوجد اي مفتاح محفوظ")
        return
    
    text = "\n".join([f"👤 {name}: {path}" for name, path in contacts.items()])
    messagebox.showinfo("اسماء المفاتيح", text)
# إنشاء النافذة الرئيسية
window = tk.Tk()
window.title("Secure File Storage")
window.geometry("400x500")
window.resizable(False, False)

# العنوان
title = tk.Label(
    window,
    text="🔐 Secure File Storage",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

subtitle = tk.Label(
    window,
    text="( AES + RSA Hybrid Encryption )",
    font=("Arial", 10)
)
subtitle.pack()
# إطار للأزرار
frame = tk.Frame(window)
frame.pack(pady=30)

# زر التشفير
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

# زر فك التشفير
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

# زر إضافة جهة اتصال
btn_add = tk.Button(
    frame,
    text="👤 Add Contact",
    font=("Arial", 12),
    width=25,
    height=2,
    bg="#FF9800",
    fg="white",
    command=add_contact_action
)
btn_add.pack(pady=10)

# زر عرض جهات الاتصال
btn_list = tk.Button(
    frame,
    text="📋 List Contacts",
    font=("Arial", 12),
    width=25,
    height=2,
    bg="#9C27B0",
    fg="white",
    command=list_contacts_action
)
btn_list.pack(pady=10)
window.mainloop()
