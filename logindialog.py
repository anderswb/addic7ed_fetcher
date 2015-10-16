import tkinter as tk
import dialog
from tkinter import ttk
import login
from tkinter import messagebox

__author__ = 'Anders'


class LoginDialog(dialog.Dialog):

    def __init__(self, parent, model, title=None):
        dialog.Dialog.__init__(self, parent, title)
        self.model = model

    def body(self, master):

        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)

        self.e1 = ttk.Entry(master)
        self.e2 = ttk.Entry(master, show="*")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def validate(self):
        try:
            self.model.login(self.e1.get(), self.e2.get())
            return True
        except TypeError as e:
            messagebox.showerror('Login error', e)
            return False

    def apply(self):
        pass
