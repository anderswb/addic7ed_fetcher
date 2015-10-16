import tkinter as tk
from tkinter import messagebox

import dialogs.logindialog as logindialog

from pages.selectshowpage import SelectShowPage as SelectShowPage
from pages.subtitleselectionpage import SubtitleSelectionPage as SubtitleSelectionPage

__author__ = 'Anders'


class View:

    def __init__(self, controller, master):
        self.master = master

        container = tk.Frame(master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.menu = Menu(controller, master)

        self.frames = {}
        for page in (SelectShowPage, SubtitleSelectionPage):
            frame = page(container, controller)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(SelectShowPage)

    def show_frame(self, content):
        frame = self.frames[content]
        frame.updatedisplay()
        frame.tkraise()

    def settitle(self, title):
        self.master.title(title)

    def showlogindialog(self, model):
        return logindialog.LoginDialog(self.master, model, title='Login')

    def showaboutdialog(self):
        messagebox.showinfo("About", "Addic7ed.com fetcher\n"
                                     "By Anders Brandt")

    def clearshows(self):
        self.frames[SelectShowPage].showslistbox.delete(0, 'end')

    def addshow(self, show):
        self.frames[SelectShowPage].showslistbox.insert(tk.END, show)


class Menu:

    def __init__(self, controller, master):
        self.controller = controller
        self.menubar = tk.Menu(master)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Login...", command=lambda: self.pressed('login'))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=lambda: self.pressed('exit'))
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        helpmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: self.pressed('about'))

        self.menubar.add_cascade(label="Help", menu=helpmenu)

        tk.Tk.config(master, menu=self.menubar)

    def pressed(self, item):
        self.controller.menuitempressed(item)
