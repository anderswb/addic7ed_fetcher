import tkinter as tk
from tkinter import ttk
from fetchandparse import fetchAndParse
from tkinter.font import Font
import addic7ed_fetcher
import subtitleselectionpage
from fnmatch import fnmatch

__author__ = 'Anders'

class SelectShowPage(tk.Frame):

    def updatelist(self, searchterm):
        self.listbox1.delete(0, 'end')
        for show in self.shows:
            if fnmatch(show[1].lower(), searchterm.lower()):
                self.listbox1.insert(0, show[1])

    def nextpage(self, controller):
        selection = self.listbox1.curselection()
        if len(selection) > 0:
            selectedshowtitle = self.listbox1.get(selection[0])
            selectedshow = [self.shows[i] for i, v in enumerate(self.shows) if v[1] == selectedshowtitle][0]
            subtitleselectionpage.SubtitleSelectionPage.updatedisplay(self,selectedshow)
            controller.show_frame(subtitleselectionpage.SubtitleSelectionPage)
        else:
            popupmsg("Error", "Please make a selection!")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Select a show:")

        searchentry = ttk.Entry(self)
        searchentry.insert(0, '*')
        searchentry.bind("<Return>",(lambda event: self.updatelist(searchentry.get())))

        label2 = ttk.Label(self, text="Search:")
        self.shows = fetchAndParse.getshows(self)

        scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.listbox1 = tk.Listbox(self, width=50, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox1.yview)
        self.updatelist('*')

        button1 = ttk.Button(self, text="Ok...",
                             command=lambda: self.nextpage(controller))

        label1.grid(row=0)
        searchentry.grid(row=1, sticky='ew', columnspan=2)
        self.listbox1.grid(row=2, column=0, sticky='nsew')
        scrollbar.grid(row=2, column=1, sticky='nse')
        button1.grid(row=3)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_rowconfigure(self, 2, weight=1)

