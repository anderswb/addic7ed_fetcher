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
        #DownloadDialog.progresslabel = tk.Label(master, text="Download progress label")
        DownloadDialog.statustree.grid(row=0)
        #DownloadDialog.progresslabel.grid(row=1)
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
        child = DownloadDialog.statustree.get_children()[index]
        season = DownloadDialog.statustree.item(child)['values'][1]
        episode = DownloadDialog.statustree.item(child)['values'][2]
        DownloadDialog.statustree.item(child, values=[status, season, episode])

    def apply(self):
        pass

