import tkinter as Tk
from model import Model
from view import View
from tkinter import messagebox

from selectshowpage import SelectShowPage
from subtitleselectionpage import SubtitleSelectionPage

__author__ = 'Anders'


class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.view = View(self, self.root)  # create the view object
        self.root.geometry("500x300")
        self.root.minsize(width=500, height=300)

        self.model = Model(self.view)  # create the model object

        # SELECTSHOWPAGE SETUP
        self.view.frames[SelectShowPage].searchentry.bind("<Return>", self.selectshowpage_filterchanged)

        # SUBTITLESELECTIONPAGESETUP

        # bind the subtitleselectionpage buttons to actions
        self.view.frames[SubtitleSelectionPage].buttonpanel.buttons['Back'].bind('<Button-1>', self.showsubtitlespage_backbutton)

    def run(self):
        self.root.title("addic7ed Fetcher")
        self.root.deiconify()
        self.root.mainloop()

    def menuitempressed(self, item):
        if item == 'login':
            logindialog = self.view.showlogindialog()  # show the dialog

            # bind the buttons
            logindialog.okbutton.bind('<Button>', self.login_okpressed)
            logindialog.cancelbutton.bind('<Button>', self.login_cancelpressed)

            # wait until the window has been closed, for one reason or another
            logindialog.wait_window(logindialog)

        elif item == 'about':
            self.view.showaboutdialog()
        elif item == 'exit':
            self.quitprogram()
        else:
            print('Unknown menu item: ' + item)

    def selectshowpage_okpressed(self, event=None):
        selectedshow = self.view.frames[SelectShowPage].showslistbox.curselection()[0]
        self.model.displayshow(selectedshow)
        self.view.show_frame(SubtitleSelectionPage)

    def selectshowpage_exitpressed(self):
        quit()

    def showsubtitlespage_backbutton(self, event=None):
        self.view.show_frame(SelectShowPage)

    def selectshowpage_filterchanged(self, event):
        filterstring = self.view.frames[SelectShowPage].searchentry.get()
        self.model.updateshowlist(filterstring)

    def login_okpressed(self, event):
        print('ok')

    def login_cancelpressed(self, event):
        print('cancel')

    def quitprogram(self, event=None):
        exit()
