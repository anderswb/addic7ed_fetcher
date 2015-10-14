__author__ = 'Anders'

import tkinter as tk
from tkinter import ttk

__author__ = 'Anders'


class Page(tk.Frame):

    def updatedisplay(self):
        pass

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Please override the __init__ method")

        label1.pack(side=tk.TOP)

        self.bottompanel = ButtonPanel(self, buttons=('OK', 'Exit'))
        self.bottompanel.pack(side=tk.BOTTOM, fill=tk.X)


class ButtonPanel(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        passed_buttons = []
        for button in kw.pop('buttons', None):
            passed_buttons.append(button)

        tk.Frame.__init__(self, master, cnf, **kw)

        self.buttons = []
        for i, button in enumerate(passed_buttons):
            self.buttons.append(ttk.Button(self, text=button))
            self.buttons[i].pack(side=tk.RIGHT, padx=5, pady=2)
