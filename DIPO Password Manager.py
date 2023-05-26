import json
import getpass
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

PASSWORDS_FILE = "C:/Password Manager/saved_password/passwords.json"

def load_passwords():
    if not os.path.isfile(PASSWORDS_FILE):
        os.makedirs(os.path.dirname(PASSWORDS_FILE), exist_ok=True)
        with open(PASSWORDS_FILE, 'w') as file:
            file.write("{}")
    try:
        with open(PASSWORDS_FILE, 'r') as file:
            passwords = json.load(file)
    except FileNotFoundError:
        passwords = {}
    return passwords

def save_passwords(passwords):
    with open(PASSWORDS_FILE, 'w') as file:
        json.dump(passwords, file)

def add_password():
    account = account_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if account and username and password:
        if account in passwords:
            passwords[account].append({
                'username': username,
                'password': password
            })
        else:
            passwords[account] = [{
                'username': username,
                'password': password
            }]
        save_passwords(passwords)
        messagebox.showinfo("Success", "Password added successfully.")
    else:
        messagebox.showwarning("Error", "Please enter all fields.")

def get_password():
    account = account_entry.get()
    account_lower = account.lower()  # Convert account name to lowercase
    found_passwords = []
    for acc, password_data in passwords.items():
        if acc.lower() == account_lower:  # Compare lowercase account names
            found_passwords.extend(password_data)
    if found_passwords:
        password_list.delete(1.0, tk.END)
        for data in found_passwords:
            username = data['username']
            password = data['password']
            password_list.insert(tk.END, f"Username: {username}\nPassword: {password}\n\n")
    else:
        messagebox.showwarning("Error", "Account not found.")

def remove_password():
    account = account_entry.get()
    if account in passwords:
        del passwords[account]
        save_passwords(passwords)
        messagebox.showinfo("Success", "Password removed successfully.")
    else:
        messagebox.showwarning("Error", "Account not found.")

def list_passwords():
    password_list.delete(1.0, tk.END)
    if passwords:
        for account, data_list in passwords.items():
            password_list.tag_configure('bold', font=('Helvetica', 12, 'bold'))  # Configure bold tag
            password_list.insert(tk.END, f"{account}\n", 'bold')  # Apply bold tag to account name
            for data in data_list:
                if isinstance(data, dict):  # Check if data is a dictionary
                    username = data.get('username')
                    password = data.get('password')
                    if username and password:
                        password_list.insert(tk.END, f"Username: {username}\nPassword: {password}\n\n")
                    else:
                        password_list.insert(tk.END, "Invalid data format.\n\n")
                else:
                    password_list.insert(tk.END, "Invalid data format.\n\n")
    else:
        password_list.insert(tk.END, "No passwords found.")

def clear_password_list():
    password_list.delete(1.0, tk.END)

def save_and_exit():
    save_passwords(passwords)
    root.destroy()


passwords = load_passwords()

root = tk.Tk()
root.title("DIPO Password Manager")
root.iconbitmap('C:\Password Manager/favicon.ico')  # Set the program icon
root.resizable(False, False)

# Styling
style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TText", font=("Helvetica", 12))

# Account Label and Entry
account_label = ttk.Label(root, text="Account:")
account_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
account_entry = ttk.Entry(root, width=30)
account_entry.grid(row=0, column=1, padx=10, pady=5)

# Username Label and Entry
username_label = ttk.Label(root, text="Username:")
username_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
username_entry = ttk.Entry(root, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=5)

# Password Label and Entry
password_label = ttk.Label(root, text="Password:")
password_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
password_entry = ttk.Entry(root, show="*", width=30)
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
add_button = ttk.Button(root, text="Add", command=add_password)
add_button.grid(row=3, column=0, padx=10, pady=5)

get_button = ttk.Button(root, text="Search", command=get_password)
get_button.grid(row=3, column=1, padx=10, pady=5)

remove_button = ttk.Button(root, text="Remove", command=remove_password)
remove_button.grid(row=3, column=2, padx=10, pady=5)

list_button = ttk.Button(root, text="List All", command=list_passwords)
list_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

clear_button = ttk.Button(root, text="Clear", command=clear_password_list)
clear_button.grid(row=4, column=2, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

# Password List
password_list = tk.Text(root, width=50, height=10)
password_list.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)


# Load initial passwords in the list
list_passwords()

root.protocol("WM_DELETE_WINDOW", save_and_exit)

# Copyright Label
copyright_label = tk.Label(root, text="© 2023 Zuharman - IT DIPO Gatsu")
copyright_label.grid(row=6, column=0, columnspan=3, pady=10)

# Clear password list at the beginning of each session
clear_password_list()

# Save passwords when the program exits
root.mainloop()

# Save passwords before exiting
save_passwords(passwords)

