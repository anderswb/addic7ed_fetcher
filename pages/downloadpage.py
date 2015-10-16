import tkinter as tk
from tkinter import ttk

import pages.page as page

from tkinter.font import Font

__author__ = 'Anders'


class DownloadPage(page.Page):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        columns = ['Status', 'Season', 'Episode']
        self.statustree = ttk.Treeview(self, columns=columns, show='headings')
        self.statustree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        for column in columns:
            self.statustree.heading(column, text=column.title())
            self.statustree.column(column, width=Font().measure(column.title()))

        self.statustree.tag_configure('white', background='white')
        self.statustree.tag_configure('green', background='pale green')
        self.statustree.tag_configure('red', background='tomato')
        self.statustree.tag_configure('yellow', background='yellow')

        self.buttonpanel = page.ButtonPanel(self, buttons=('OK', 'Cancel', 'Back'),
                                            commands=(controller.downloadpage_okpressed,
                                                      controller.downloadpage_cancelpressed,
                                                      controller.downloadpage_backpressed),
                                            states=(tk.DISABLED, tk.ACTIVE, tk.DISABLED))
        self.buttonpanel.pack(side=tk.BOTTOM, fill=tk.X)
