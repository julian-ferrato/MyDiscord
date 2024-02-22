import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My Discord")
        self.geometry("400x300")

        self.create_widgets()

        self.conn = sqlite3.connect('myDiscord.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           firstname TEXT,
                           name TEXT,
                           email TEXT,
                           password TEXT)''')
        self.conn.commit()

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self, text="Email :")
        self.label_username.pack()

        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = tk.Label(self, text="Mot de passe :")
        self.label_password.pack()

        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.btn_login = tk.Button(self, text="Connexion", command=self.login)
        self.btn_login.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top", fill="x")

        self.btn_close = tk.Button(self.button_frame, text="x", command=self.quit)
        self.btn_close.pack(side="left", padx=(10, 0), pady=(5, 0))

        self.btn_register = tk.Button(self, text="S'inscrire", command=self.open_register_page)
        self.btn_register.pack()
        

    def login(self):

        messagebox.showinfo("Réussite","Connexion réussie!")

    def open_register_page(self):
        self.withdraw() 
        register_page = RegisterPage(self)  

        
class RegisterPage(tk.Toplevel):
    def __init__(self, login_page):
        super().__init__(login_page)
        self.login_page = login_page
        self.title("Register")
        self.geometry("400x300")
        self.create_widgets()   

    def create_widgets(self):
        self.lbl_firstname = tk.Label(self, text="Prénom :")
        self.lbl_firstname.pack()

        self.entry_firstname = tk.Entry(self)  
        self.entry_firstname.pack()

        self.lbl_name = tk.Label(self, text="Nom :")
        self.lbl_name.pack()

        self.entry_name = tk.Entry(self)  
        self.entry_name.pack()

        self.label_email = tk.Label(self, text="Email :")
        self.label_email.pack()

        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        self.label_password = tk.Label(self, text="Mot de passe :")
        self.label_password.pack()

        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.btn_back = tk.Button(self, text="<", command=self.go_to_login)
        self.btn_back.place(relx=0.05, rely=0.05, anchor="ne")

        self.btn_submit = tk.Button(self, text="S'inscrire", command=self.register)
        self.btn_submit.pack()
        

    def go_to_login(self):
        self.destroy()
        self.login_page.deiconify()    

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        name = self.entry_name.get()

        user_info = {
            "name": name,
        }

        firstname = self.entry_firstname.get()

        user_info = {
            "firstname": firstname,
        }

        if not firstname or not name or not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tout les champs.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erreur", "Veuillez entrer une adresse mail valide.")
            return
        
        if not self.check_password_strength(password):
            messagebox.showerror("Erreur", "Le mot de passe ne répond pas aux critères de sécurité.")
            return

        messagebox.showinfo("Réussite","Inscription réussie!")
        self.destroy()
        self.login_page.deiconify()

    def check_password_strength(self, password):
         if len(password) < 7:
            return False

         if not re.search(r'[!@#$%^&*()_+{}|:"<>?]', password):
            return False

         if not re.search(r'[A-Z]', password):
            return False

         if not re.search(r'\d', password):
            return False

         return True

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()

app = Application()
app.mainloop() 