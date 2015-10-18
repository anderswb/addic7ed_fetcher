import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

import pages.page as page

__author__ = 'Anders'


class SubtitleSelectionPage(page.Page):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.label = tk.StringVar()
        label1 = ttk.Label(self, text="Unknown show", textvariable=self.label)
        self.notebook = ttk.Notebook(self)
        self.filterpanel = FilterPanel(self)
        self.buttonpanel = page.ButtonPanel(self, buttons=('Download', 'Back'),
                                            commands=(controller.subtitleselectionpage_downloadpressed,
                                                      controller.subtitleselectionpage_backpressed))

        # Packing
        label1.pack(side=tk.TOP)
        self.filterpanel.pack(side=tk.TOP, fill=tk.X)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.buttonpanel.pack(side=tk.BOTTOM, fill=tk.X)

    def addtab(self, season):
        columns = ('ep', 'name', 'lang', 'vers', 'completed', 'hi', 'corrected', 'hd')

        frame = ttk.Frame(self.notebook)  # use the notebook frame

        # add new tab, with the name of the season
        self.notebook.add(frame, text="S{:02}".format(season))

        # Create a treeview for the current season, and add it to the tab
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.grid(row=0, column=0, sticky='nsew')  # add the tree to the view

        # Create y scrollbar, and add it to the tree and grid
        ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky='ns')

        # make sure that the frame takes up the entire room in the notebook tab
        tk.Grid.grid_rowconfigure(frame, 0, weight=1)
        tk.Grid.grid_columnconfigure(frame, 0, weight=1)

        # Put in the headings on the new tree
        for column in columns:
            tree.heading(column, text=column.title())

        # configure the tags used for alternating the colors of the rows
        tree.tag_configure('white', background='white')
        tree.tag_configure('gray', background='lightgray')

        return tree


class FilterPanel(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master

        # Setup the checkboxes
        self.hi = tk.StringVar(value='off')
        self.hd = tk.StringVar(value='off')
        self.corrected = tk.StringVar(value='off')

        self.check_hi = ttk.Checkbutton(self, text="HI", variable=self.hi, command=self.hichanged,
                                        onvalue='on', offvalue='off')
        self.check_hd = ttk.Checkbutton(self, text="HD", variable=self.hd, command=self.hdchanged,
                                        onvalue='on', offvalue='off')
        self.check_cor = ttk.Checkbutton(self, text="Corrected", variable=self.corrected, command=self.corchanged,
                                         onvalue='on', offvalue='off')

        self.hd.set(value='dontcare')
        self.check_hd.state(['alternate'])
        self.last_hd_state = 'dontcare'

        self.hi.set(value='dontcare')
        self.check_hi.state(['alternate'])
        self.last_hi_state = 'dontcare'

        self.corrected.set(value='dontcare')
        self.check_cor.state(['alternate'])
        self.last_cor_state = 'dontcare'

        # Setup the dropdown menu
        self.language = tk.StringVar(self)
        self.language.set("All languages")  # default value
        self.dropdown = ttk.OptionMenu(self, self.language)
        self.languageselected = 'All languages'

        self.check_hi.grid(row=0, column=0, sticky='w', padx=10)
        self.check_hd.grid(row=0, column=1, sticky='w', padx=10)
        self.check_cor.grid(row=0, column=2, sticky='w', padx=10)
        self.dropdown.grid(row=0, column=3, sticky='e', padx=10)
        tk.Grid.grid_columnconfigure(self, 3, weight=1)

    def hdchanged(self):
        self.last_hd_state = self.checkboxchange(self.last_hd_state, self.hd, self.check_hd)
        self.filterchanged()

    def hichanged(self):
        self.last_hi_state = self.checkboxchange(self.last_hi_state, self.hi, self.check_hi)
        self.filterchanged()

    def corchanged(self):
        self.last_cor_state = self.checkboxchange(self.last_cor_state, self.corrected, self.check_cor)
        self.filterchanged()

    def language_dropdownchanged(self, language):
        self.language.set(language)
        self.filterchanged()

    def filterchanged(self):
        self.master.controller.subtitleselectionpage_filterchanged()

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
