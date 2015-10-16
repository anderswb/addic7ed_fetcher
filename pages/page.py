__author__ = 'Anders'

import tkinter as tk
from tkinter import ttk

__author__ = 'Anders'


class Page(tk.Frame):

    def updatedisplay(self):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Please override the __init__ method")

        label1.pack(side=tk.TOP)

        self.bottompanel = ButtonPanel(self, buttons=('OK', 'Exit'))
        self.bottompanel.pack(side=tk.BOTTOM, fill=tk.X)


class ButtonPanel(tk.Frame):

    def __init__(self, master, buttons, cnf={}, commands=None):
        tk.Frame.__init__(self, master, cnf)

        self.buttons = {}
        for i, button in enumerate(buttons):
            if commands is None:
                self.buttons[button] = ttk.Button(self, text=button)
                self.buttons[button].pack(side=tk.RIGHT, padx=5, pady=2)
            else:
                self.buttons[button] = ttk.Button(self, text=button, command=commands[i])
                self.buttons[button].pack(side=tk.RIGHT, padx=5, pady=2)
