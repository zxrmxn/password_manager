import json
import tkinter as tk
from tkinter import messagebox, ttk
import os

# Define passwords.json and users.json to spesific directory
PASSWORDS_DIR = "C:/Password Manager/saved_password/"
USERS_FILE = os.path.join(PASSWORDS_DIR, "users.json")

# Create the password directory if it doesn't exist
os.makedirs(PASSWORDS_DIR, exist_ok=True)

# Load the .json file to retrieve the data inside
def load_data(filename):
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            file.write("{}")
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

# Write input data into .json file
def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

# Register Function
def register():
    username = register_username_entry.get()
    password = register_password_entry.get()
    if username and password:
        if username in users:
            messagebox.showwarning("Registration Failed", "Username already exists.")
        else:
            users[username] = {'password': password, 'passwords_file': os.path.join(PASSWORDS_DIR, f"{username}.json")}
            save_data(users, USERS_FILE)
            save_data({}, users[username]['passwords_file'])  # Create an empty passwords file for the user
            messagebox.showinfo("Registration Successful", "You have been registered successfully.")
            clear_register_form()
    else:
        messagebox.showwarning("Registration Failed", "Please enter both username and password.")

# Login Function
def login(root):
    global logged_in_user
    username = login_username_entry.get()
    password = login_password_entry.get()
    if username and password:
        if username in users and users[username]['password'] == password:
            logged_in_user = username
            clear_login_form()
            root.destroy()

            # Main Program (Password Manager) Goes here

            # Create .json file if it's not exist with empty dictionary
            def load_passwords():
                if logged_in_user in users:
                    passwords_file = users[logged_in_user]['passwords_file']
                    if not os.path.isfile(passwords_file):
                        with open(passwords_file, 'w') as file:
                            file.write("{}")
                    try:
                        with open(passwords_file, 'r') as file:
                            passwords = json.load(file)
                    except FileNotFoundError:
                        passwords = {}
                    return passwords
                else:
                    messagebox.showwarning("Login Failed", "Invalid user.")
                    return {}

            # Saving function to save Python dictionary into a .json file
            def save_passwords(passwords):
                if logged_in_user in users:
                    passwords_file = users[logged_in_user]['passwords_file']
                    with open(passwords_file, 'w') as file:
                        json.dump(passwords, file)

            # Function to add a new password into a .json file
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

            # Function to search a spesific password in a dictionary
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

            # Function to remove a spesific password in a dictionary
            def remove_password():
                account = account_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                if account and username and password:
                    if account in passwords:
                        account_passwords = passwords[account]
                        found = False
                        for data in account_passwords:
                            if data['username'] == username and data['password'] == password:
                                account_passwords.remove(data)
                                found = True
                                break
                        if found:
                            if len(account_passwords) == 0:
                                del passwords[account]
                            save_passwords(passwords)
                            messagebox.showinfo("Success", "Password removed successfully.")
                        else:
                            messagebox.showwarning("Error", "Specified password not found.")
                    else:
                        messagebox.showwarning("Error", "Account not found.")
                else:
                    messagebox.showwarning("Error", "Please enter all fields.")

            def edit_password():
                account = account_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                if account and username and password:
                    if account in passwords:
                        account_passwords = passwords[account]
                        found = False
                        for data in account_passwords:
                            if data['username'] == username:
                                data['password'] = password
                                found = True
                                break
                        if found:
                            save_passwords(passwords)
                            messagebox.showinfo("Success", "Password edited successfully.")
                        else:
                            messagebox.showwarning("Error", "Specified username not found.")
                    else:
                        messagebox.showwarning("Error", "Account not found.")
                else:
                    messagebox.showwarning("Error", "Please enter all fields.")

            # Function to list all the saved password in dictionary and shown all of it in list password field
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

            # Clear listed password
            def clear_password_list():
                password_list.delete(1.0, tk.END)

            # Function to save when close the program
            def save_and_exit():
                save_passwords(passwords)
                root.destroy()

            # Visibility function to show censored password
            def toggle_password_visibility():
                if password_entry['show'] == '*':
                    password_entry.config(show='')
                    visibility_button.config(text='Hide')
                else:
                    password_entry.config(show='*')
                    visibility_button.config(text='Show')

            passwords = load_passwords()

            root = tk.Tk()
            root.title("Password Manager")
            root.iconbitmap('C:\Password Manager/favicon.ico')  # Set the program icon
            root.resizable(False, False)

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

            # Visibility Button
            visibility_button = ttk.Checkbutton(root, text="Show", command=toggle_password_visibility)
            visibility_button.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

            # Buttons
            add_button = ttk.Button(root, text="Add Password", command=add_password)
            add_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)

            get_button = ttk.Button(root, text="Search", command=get_password)
            get_button.grid(row=3, column=0, padx=10, pady=5)

            edit_button = ttk.Button(root, text="Edit", command=edit_password)
            edit_button.grid(row=3, column=1, padx=10, pady=5)

            remove_button = ttk.Button(root, text="Remove", command=remove_password)
            remove_button.grid(row=3, column=2, padx=10, pady=5)

            list_button = ttk.Button(root, text="List All Password", command=list_passwords)
            list_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)

            clear_button = ttk.Button(root, text="Clear List Password", command=clear_password_list)
            clear_button.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)

            # Password List
            password_list = tk.Text(root, width=50, height=10)
            password_list.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)

            # Load initial passwords in the list
            list_passwords()

            root.protocol("WM_DELETE_WINDOW", save_and_exit)

            # Copyright Label
            copyright_label = tk.Label(root, text="© 2023 Zuharman - IT DIPO Gatsu")
            copyright_label.grid(row=8, column=0, columnspan=3, pady=10)

            # Clear password list at the beginning of each session
            clear_password_list()

            # Save passwords when the program exits
            root.mainloop()

            # Save passwords before exiting
            save_passwords(passwords)

            root.mainloop()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password.")
    else:
        messagebox.showwarning("Login Failed", "Please enter both username and password.")

# Bind Enter keys to confirm in login and register windows
def bind_enter_keys():
    register_username_entry.bind('<Return>', lambda event: register())
    register_password_entry.bind('<Return>', lambda event: register())
    login_username_entry.bind('<Return>', lambda event: login(root))
    login_password_entry.bind('<Return>', lambda event: login(root))

# Clear register and login form when first open and when switch tab between those 2
def clear_register_form():
    register_username_entry.delete(0, tk.END)
    register_password_entry.delete(0, tk.END)

def clear_login_form():
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)

users = load_data(USERS_FILE)

root = tk.Tk()
root.title("Password Manager")
root.iconbitmap('C:\Password Manager/favicon.ico')  # Set the program icon
root.resizable(False, False)

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10)

# Styling
style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TText", font=("Helvetica", 12))

# Login Tab
login_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="Login")

login_label = ttk.Label(login_tab, text="Login")
login_label.pack(padx=10, pady=10)

login_username_label = ttk.Label(login_tab, text="Username:")
login_username_label.pack(padx=10, pady=5)
login_username_entry = ttk.Entry(login_tab, width=30)
login_username_entry.pack(padx=10, pady=5)

login_password_label = ttk.Label(login_tab, text="Password:")
login_password_label.pack(padx=10, pady=5)
login_password_entry = ttk.Entry(login_tab, show="*", width=30)
login_password_entry.pack(padx=10, pady=5)

login_button = ttk.Button(login_tab, text="Login", command=lambda: login(root))
login_button.pack(padx=10, pady=10)

# Register Tab
register_tab = ttk.Frame(notebook)
notebook.add(register_tab, text="Register")

register_label = ttk.Label(register_tab, text="Register")
register_label.pack(padx=10, pady=10)

register_username_label = ttk.Label(register_tab, text="Username:")
register_username_label.pack(padx=10, pady=5)
register_username_entry = ttk.Entry(register_tab, width=30)
register_username_entry.pack(padx=10, pady=5)

register_password_label = ttk.Label(register_tab, text="Password:")
register_password_label.pack(padx=10, pady=5)
register_password_entry = ttk.Entry(register_tab, show="*", width=30)
register_password_entry.pack(padx=10, pady=5)

register_button = ttk.Button(register_tab, text="Register", command=register)
register_button.pack(padx=10, pady=10)

root.after(0, bind_enter_keys)

root.mainloop()
