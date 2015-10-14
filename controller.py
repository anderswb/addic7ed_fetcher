import tkinter as Tk
from model import Model
from view import View
from tkinter import messagebox

__author__ = 'Anders'


class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()  # create the model object
        self.view = View(self, self.root)  # create the view object
        self.root.geometry("500x300")

        # bind the view buttons to actions in the controller
        #self.view.bottompanel.okbutton.bind("<Button>", self.updatelabel)
        #self.view.bottompanel.exitbutton.bind("<Button>", self.quitprogram)

        #self.view.menu.menubar.bind("<<MenuSelect>>", self.menucallback)

    def run(self):
        self.root.title("addic7ed MVC Fetcher")
        self.root.deiconify()
        self.root.mainloop()

    def menuitempressed(self, item):
        if item == 'login':
            pass
        elif item == 'about':
            messagebox.showinfo("About", "Addic7ed.com fetcher\n"
                                         "By Anders Brandt")
        elif item == 'exit':
            self.quitprogram()
        else:
            print('Unknown item: ' + item)

    def menucallback(self, event):
        widget = self.root.nametowidget(event.widget[2:])
        print(type(widget))
        print(self.view.menu.filemenu.index())

        #print(m.entrycget(m.index('@%d' % event.y), 'label'))
        print('hej')
        #print(self.view.menu.filemenu.index('last'))
        #print(self.root.call(event.widget, "index", "active") )
        #widget = self.root.nametowidget(event.widget[2:])
        #print(type(widget))
        #print(widget.index(Tk.ACTIVE))
        #print(self.root.call(event.widget, "index", "Exit"))

    def quitprogram(self):
        exit()

    def updatelabel(self, event):
        self.model.calculate()
        self.view.label.set(self.model.res)
