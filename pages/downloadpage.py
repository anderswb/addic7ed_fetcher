import tkinter as tk
from tkinter import ttk

import pages.page as page

__author__ = 'Anders'


class DownloadPage(page.Page):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        self.buttonpanel = page.ButtonPanel(self, buttons=('OK', 'Back'),
                                            commands=[controller.selectshowpage_okpressed,
                                                      controller.selectshowpage_exitpressed])
        self.buttonpanel.pack(side=tk.BOTTOM, fill=tk.X)

