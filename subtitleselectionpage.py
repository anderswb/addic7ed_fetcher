import tkinter as tk
from tkinter import ttk
from fetchandparse import FetchAndParse
from tkinter.font import Font
import selectshowpage
from downloaddialog import DownloadDialog
from downloadsession import session
from tkinter import messagebox
from re import findall
from threading import Thread
import time

import page

__author__ = 'Anders'


class SubtitleSelectionPage(page.Page):


    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        SubtitleSelectionPage.label1 = ttk.Label(self, text="Unknown show")

        SubtitleSelectionPage.notebook = ttk.Notebook(self)

        # Setup the checkboxes
        self.hivar = tk.StringVar(value='off')
        self.hdvar = tk.StringVar(value='off')
        self.corvar = tk.StringVar(value='off')

        nestedframe = tk.Frame(self)
        self.check_hi = ttk.Checkbutton(nestedframe, text="HI", variable=self.hivar, command=self.hichanged,
                                        onvalue='on', offvalue='off')
        self.check_hd = ttk.Checkbutton(nestedframe, text="HD", variable=self.hdvar, command=self.hdchanged,
                                        onvalue='on', offvalue='off')
        self.check_cor = ttk.Checkbutton(nestedframe, text="Corrected", variable=self.corvar, command=self.corchanged,
                                         onvalue='on', offvalue='off')

        self.hdvar.set(value='dontcare')
        self.check_hd.state(['alternate'])
        self.last_hd_state = 'dontcare'

        self.hivar.set(value='dontcare')
        self.check_hi.state(['alternate'])
        self.last_hi_state = 'dontcare'

        self.corvar.set(value='dontcare')
        self.check_cor.state(['alternate'])
        self.last_cor_state = 'dontcare'

        # Setup the dropdown menu
        self.dropdownvar = tk.StringVar(self)
        self.dropdownvar.set("All languages")  # default value
        self.dropdown = ttk.OptionMenu(nestedframe, self.dropdownvar, "All languages")

        # create button panel
        self.buttonpanel = page.ButtonPanel(self, buttons=('Download', 'Back'))
        self.buttonpanel.pack(side=tk.BOTTOM, fill=tk.X)

        # Packing
        SubtitleSelectionPage.label1.pack(side=tk.TOP)

        nestedframe.pack(side=tk.TOP, fill=tk.X)

        self.check_hi.grid(row=0, column=0, sticky='w', padx=10)
        self.check_hd.grid(row=0, column=1, sticky='w', padx=10)
        self.check_cor.grid(row=0, column=2, sticky='w', padx=10)
        self.dropdown.grid(row=0, column=3, sticky='e', padx=10)
        tk.Grid.grid_columnconfigure(nestedframe, 3, weight=1)

        SubtitleSelectionPage.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def hdchanged(self):
        self.last_hd_state = self.checkboxchange(self.last_hd_state, self.hdvar, self.check_hd)

    def hichanged(self):
        self.last_hi_state = self.checkboxchange(self.last_hi_state, self.hivar, self.check_hi)

    def corchanged(self):
        self.last_cor_state = self.checkboxchange(self.last_cor_state, self.corvar, self.check_cor)

    @staticmethod
    def checkboxchange(last_state, variable_ref, checkbox_ref):
        new_state = last_state  # make sure it's set to something
        if last_state == 'off':
            variable_ref.set(value='dontcare')
            checkbox_ref.state(['alternate'])
            new_state = 'dontcare'
        elif last_state == 'dontcare':
            variable_ref.set(value='on')
            new_state = 'on'
        elif last_state == 'on':
            variable_ref.set(value='off')
            new_state = 'off'

        return new_state
