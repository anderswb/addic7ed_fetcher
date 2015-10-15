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

        # bind the selectshowpage view buttons to actions in the controller
        self.view.frames[SelectShowPage].buttonpanel.buttons['Exit'].bind('<Button>', self.quitprogram)
        self.view.frames[SelectShowPage].buttonpanel.buttons['OK'].bind('<Button>', self.showselected)

    def run(self):
        self.root.title("addic7ed Fetcher")
        self.root.deiconify()
        self.root.mainloop()

    def menuitempressed(self, item):
        if item == 'login':
            pass
        elif item == 'about':
            self.view.showaboutdialog()
        elif item == 'exit':
            self.quitprogram()
        else:
            print('Unknown item: ' + item)

    def showselected(self, event=None):
        self.view.show_frame(SubtitleSelectionPage)

    def quitprogram(self, event=None):
        exit()

    def updatelabel(self, event):
        self.model.calculate()
        self.view.label.set(self.model.res)
