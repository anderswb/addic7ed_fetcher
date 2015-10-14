import tkinter as tk
from tkinter import ttk

import page

__author__ = 'Anders'


class SelectShowPage(page.Page):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Select a show:")

        searchentry = ttk.Entry(self)
        searchentry.insert(0, '*')

        label1.pack(side=tk.TOP)
        searchentry.pack(side=tk.TOP, fill=tk.X)

        frame = tk.Frame(self)
        self.listbox1 = tk.Listbox(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.listbox1.yview)
        self.listbox1.configure(yscroll=ysb.set)
        self.listbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        for i in range(1,100):
            self.listbox1.insert(0, i)

        self.bottompanel = page.ButtonPanel(self, buttons=('OK', 'Exit'))
        self.bottompanel.pack(side=tk.BOTTOM, fill=tk.X)
