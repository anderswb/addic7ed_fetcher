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
        self.model = Model()  # create the model object
        self.view = View(self, self.root)  # create the view object
        self.root.geometry("500x300")
        self.root.minsize(width=500, height=300)

        # SELECTSOHWPAGE SETUP

        # bind the selectshowpage view buttons to actions in the controller
        self.view.frames[SelectShowPage].buttonpanel.buttons['Exit'].bind('<Button-1>', self.quitprogram)
        self.view.frames[SelectShowPage].buttonpanel.buttons['OK'].bind('<Button-1>', self.showselected)

        # fill up the shows list
        for show in self.model.get_shows():
            self.view.addshow(show[1])  # pass the show title to the view


        # SUBTITLESELECTIONPAGESETUP

        # bind the subtitleselectionpage buttons to actions
        self.view.frames[SubtitleSelectionPage].buttonpanel.buttons['Back'].bind('<Button-1>', self.backbutton)

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

    def showselected(self, event=None):
        selectedshow = self.view.frames[SelectShowPage].showslistbox.curselection()[0]
        print(self.model.indextoshow(selectedshow))
        #self.view.show_frame(SubtitleSelectionPage)

    def backbutton(self, event=None):
        self.view.show_frame(SelectShowPage)

    def login_okpressed(self, event):
        print('ok')

    def login_cancelpressed(self, event):
        print('cancel')

    def quitprogram(self, event=None):
        exit()

    def updatelabel(self, event):
        self.model.calculate()
        self.view.label.set(self.model.res)
