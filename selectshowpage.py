import tkinter as tk
from tkinter import ttk

import page

__author__ = 'Anders'


class SelectShowPage(page.Page):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Select a show:")

        self.searchentry = ttk.Entry(self)
        self.searchentry.insert(0, '*')

        label1.pack(side=tk.TOP)
        self.searchentry.pack(side=tk.TOP, fill=tk.X)

        frame = tk.Frame(self)
        self.showslistbox = tk.Listbox(frame)
        self.showslistbox.bind('<Double-Button-1>', controller.selectshowpage_okpressed)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.showslistbox.yview)
        self.showslistbox.configure(yscroll=ysb.set)
        self.showslistbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.buttonpanel = page.ButtonPanel(self, buttons=('OK', 'Exit'),
                                            commands=[controller.selectshowpage_okpressed,
                                                      controller.selectshowpage_exitpressed])
        self.buttonpanel.pack(side=tk.BOTTOM, fill=tk.X)
