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

        self.model.updatetitle()

        # SELECTSHOWPAGE SETUP
        self.view.frames[SelectShowPage].searchentry.bind("<Return>", self.selectshowpage_filterchanged)

        # SUBTITLESELECTIONPAGE SETUP

    def run(self):
        self.root.deiconify()
        self.root.mainloop()

    def menuitempressed(self, item):
        if item == 'login':
            self.logindialog = self.view.showlogindialog(self.model)  # show the dialog
            # wait until the window has been closed, for one reason or another
            self.logindialog.wait_window(self.logindialog)
            self.model.updatetitle()
        elif item == 'about':
            self.view.showaboutdialog()
        elif item == 'exit':
            self.quitprogram()
        else:
            print('Unknown menu item: ' + item)

    def selectshowpage_okpressed(self, event=None):
        curselection = self.view.frames[SelectShowPage].showslistbox.curselection()
        if curselection:  # if an item is selected
            selectedshow = curselection[0]  # get the listbox selection
            self.model.displayshow(selectedshow)  # update the model, and in turn the view
            self.view.show_frame(SubtitleSelectionPage)  # show the new frame

    def selectshowpage_exitpressed(self):
        quit()

    def subtitleselectionpage_backpressed(self):
        self.view.show_frame(SelectShowPage)

    def selectshowpage_filterchanged(self, event):
        filterstring = self.view.frames[SelectShowPage].searchentry.get()
        self.model.updateshowlist(filterstring)

    def subtitleselectionpage_downloadpressed(self):
        print('Download pressed!')

    def quitprogram(self, event=None):
        exit()
