import tkinter as Tk
from mvc.model import Model as Model
from mvc.view import View as View

import tkinter as tk

from pages.selectshowpage import SelectShowPage as SelectShowPage
from pages.subtitleselectionpage import SubtitleSelectionPage as SubtitleSelectionPage
from pages.downloadpage import DownloadPage as DownloadPage

from threading import Thread

__author__ = 'Anders'


class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.view = View(self, self.root)  # create the view object
        self.root.geometry("500x400")
        self.root.minsize(width=500, height=400)

        self.model = Model(self.view, self)  # create the model object
        self.model.updatetitle()

        self.view.frames[SelectShowPage].searchentry.bind("<Return>", self.selectshowpage_filterchanged)

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
            self.view.show_frame(SubtitleSelectionPage)  # show the new frame
            thread = Thread(target=self.model.displayshow, args=(selectedshow, ))  # update the model, update the view
            thread.start()

    def selectshowpage_exitpressed(self):
        quit()

    def subtitleselectionpage_backpressed(self):
        self.view.show_frame(SelectShowPage)

    def selectshowpage_filterchanged(self, event):
        filterstring = self.view.frames[SelectShowPage].searchentry.get()
        self.model.updateshowlist(filterstring)

    def subtitleselectionpage_downloadpressed(self):
        self.model.add_downloads()
        thread = Thread(target=self.model.downloadandsave)
        thread.start()
        self.view.show_frame(DownloadPage)

        page = self.view.frames[DownloadPage]
        page.buttonpanel.buttons['OK'].configure(state=tk.DISABLED)
        page.buttonpanel.buttons['Cancel'].configure(state=tk.ACTIVE)
        page.buttonpanel.buttons['Back'].configure(state=tk.DISABLED)

    def subtitleselectionpage_filterchanged(self):
        self.model.updateallsubtitlelists()

    def downloadpage_okpressed(self):
        print('ok')

    def downloadpage_cancelpressed(self):
        self.model.canceldownload()

    def downloadpage_backpressed(self):
        self.view.show_frame(SubtitleSelectionPage)

    def quitprogram(self, event=None):
        exit()
