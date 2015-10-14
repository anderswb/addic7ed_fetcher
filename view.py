import tkinter as tk
from tkinter import ttk

import logindialog
import login

from selectshowpage import SelectShowPage

__author__ = 'Anders'


class View:

    def __init__(self, parent, master):
        self.master = master
        container = tk.Frame(master)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=2, pady=2)

        self.menu = Menu(parent, master)

        self.frames = {}
        for F in (SelectShowPage, ):
            frame = F(container)
            self.frames[F] = frame
            frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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
        self.updatetitle()


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
