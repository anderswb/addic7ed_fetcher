import tkinter as tk
import dialog
from tkinter import ttk
import time

__author__ = 'Anders'


class DownloadDialog(dialog.Dialog):
    statustree = None

    def __init__(self, parent, showlist, title = None):

        dialog.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body, showlist)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self, master, showlist):
        columns = ['Status', 'Season', 'Episode']
        DownloadDialog.statustree = ttk.Treeview(master, columns=columns, show='headings')
        DownloadDialog.statustree.grid(row=0)
        for column in columns:
            DownloadDialog.statustree.heading(column, text=column.title())
        DownloadDialog.populatetree(showlist)

        return None

    @staticmethod
    def populatetree(showlist):
        for show in showlist:
            list = ['Pending', show['season'], show['episode']]
            DownloadDialog.statustree.insert('', 'end', values=list)

    @staticmethod
    def updateprogress(index, status):
        children = DownloadDialog.statustree.get_children()
        child = children[index]
        season = DownloadDialog.statustree.item(child)['values'][1]
        episode = DownloadDialog.statustree.item(child)['values'][2]
        DownloadDialog.statustree.item(child, values=[status, season, episode])

        alldone = True
        for child in children:
            status = DownloadDialog.statustree.item(child)['values'][0]
            if status != 'Done' or status != 'Failure':
                alldone = False
                break

        if alldone:
            print("Done")

    def apply(self):
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
