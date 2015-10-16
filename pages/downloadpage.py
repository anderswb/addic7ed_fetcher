import tkinter as tk
from tkinter import ttk

import pages.page as page

__author__ = 'Anders'


class DownloadPage(page.Page):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        columns = ['Status', 'Season', 'Episode']
        self.statustree = ttk.Treeview(self, columns=columns, show='headings')
        self.statustree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        for column in columns:
            self.statustree.heading(column, text=column.title())
        #self.populatetree(showlist)


        self.buttonpanel = page.ButtonPanel(self, buttons=('OK', 'Back'),
                                            commands=[controller.selectshowpage_okpressed,
                                                      controller.selectshowpage_exitpressed])
        self.buttonpanel.pack(side=tk.BOTTOM, fill=tk.X)
