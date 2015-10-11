import tkinter as tk
import dialog
from tkinter import ttk
import login
from tkinter import messagebox

__author__ = 'Anders'


class LoginDialog(dialog.Dialog):

    def body(self, master):

        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)

        self.e1 = ttk.Entry(master)
        self.e2 = ttk.Entry(master, show="*")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        user = self.e1.get()
        pwd = self.e2.get()
        try:
            login.login(user, pwd)
        except TypeError as e:
            messagebox.showerror('Login error', e)
