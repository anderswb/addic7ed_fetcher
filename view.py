import tkinter as tk
from tkinter import messagebox

import logindialog
import login

from selectshowpage import SelectShowPage
from subtitleselectionpage import SubtitleSelectionPage

__author__ = 'Anders'


class View:

    def __init__(self, parent, master):
        self.master = master
        container = tk.Frame(master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.menu = Menu(parent, master)

        self.frames = {}
        for page in (SelectShowPage, SubtitleSelectionPage):
            frame = page(container)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(SelectShowPage)

    def show_frame(self, content):
        frame = self.frames[content]
        frame.updatedisplay()
        frame.tkraise()

    def updatetitle(self):
        user = login.get_current_user()
        if user is not None:
            tk.Tk.wm_title(self, "Addic7ed Fetcher - logged in as: {}".format(user))
        else:
            tk.Tk.wm_title(self, "Addic7ed Fetcher - not logged in")

    def showlogindialog(self):
        logindialog.LoginDialog(self)

    def showaboutdialog(self):
        messagebox.showinfo("About", "Addic7ed.com fetcher\n"
                                     "By Anders Brandt")


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
