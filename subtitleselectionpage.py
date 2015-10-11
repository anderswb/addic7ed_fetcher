import tkinter as tk
from tkinter import ttk
from fetchandparse import FetchAndParse
from tkinter.font import Font
import selectshowpage
from popupmessages import popupmsg

__author__ = 'Anders'


class SubtitleSelectionPage(tk.Frame):
    label1 = None
    notebook = None
    dataset_labels = ['episode', 'name', 'language', 'versions', 'completed', 'hi', 'corrected', 'hd']

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.trees = {}
        self.dataset = {}

        SubtitleSelectionPage.label1 = ttk.Label(self, text="Unknown show")

        button_back = ttk.Button(self, text="Back",
                                 command=lambda: controller.show_frame(selectshowpage.SelectShowPage))
        button_ok = ttk.Button(self, text="OK",
                               command=lambda: popupmsg(controller, "Note", "Not implemented yet!"))

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

        # Add to the grid
        SubtitleSelectionPage.label1.grid(row=0, column=0, columnspan=1)

        nestedframe.grid(row=1, column=0, sticky='we')

        self.check_hi.grid(row=0, column=0, sticky='w', padx=10)
        self.check_hd.grid(row=0, column=1, sticky='w', padx=10)
        self.check_cor.grid(row=0, column=2, sticky='w', padx=10)
        self.dropdown.grid(row=0, column=3, sticky='e', padx=10)
        tk.Grid.grid_columnconfigure(nestedframe, 3, weight=1)

        SubtitleSelectionPage.notebook.grid(row=2, column=0, columnspan=1, sticky='nsew', padx=5, pady=5)

        button_back.grid(row=3, columnspan=1, sticky='w', padx=5, pady=5)
        button_ok.grid(row=3, columnspan=1, sticky='e', padx=5, pady=5)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_rowconfigure(self, 2, weight=1)

    def updatedisplay(self):
        SubtitleSelectionPage.label1.config(text=selectshowpage.SelectShowPage.selectedshow[1])
        seasons = FetchAndParse.getseasons(selectshowpage.SelectShowPage.selectedshow[0])
        columns = ('ep', 'name', 'lang', 'vers', 'completed', 'hi', 'corrected', 'hd')

        # make sure there's no tabs displayed
        for tab in SubtitleSelectionPage.notebook.tabs():
            SubtitleSelectionPage.notebook.forget(tab)

        # populate everything
        for eachseason in seasons:
            frame = ttk.Frame(SubtitleSelectionPage.notebook)  # use the notebook frame
            SubtitleSelectionPage.notebook.add(frame, text="S{:02}".format(eachseason))

            self.trees[eachseason] = ttk.Treeview(frame, columns=columns, show='headings')
            self.trees[eachseason].grid(row=0, column=0, sticky='nsew')
            tk.Grid.grid_rowconfigure(frame, 0, weight=1)
            tk.Grid.grid_columnconfigure(frame, 0, weight=1)

            for column in columns:
                self.trees[eachseason].heading(column, text=column.title())
                self.trees[eachseason].column(column, width=Font().measure(column.title()))

            self.dataset[eachseason] = FetchAndParse.getsubtitlelist(selectshowpage.SelectShowPage.selectedshow[0],
                                                                     eachseason)
            for episodesub in self.dataset[eachseason]:
                data = []
                for label in SubtitleSelectionPage.dataset_labels:
                    data.append(episodesub[label])
                self.trees[eachseason].insert('', 'end', values=data)

        # Populate languages filter dropdown menu
        languages = FetchAndParse.getlanguages(self.dataset)
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All languages",
                         command=lambda value="All languages":
                         self.dropdownchanged(value))
        for language in languages:
            menu.add_command(label=language,
                             command=lambda value=language:
                             self.dropdownchanged(value))

    def hdchanged(self):
        if self.last_hd_state == 'off':
            self.hdvar.set(value='dontcare')
            self.check_hd.state(['alternate'])
        elif self.last_hd_state == 'dontcare':
            self.hdvar.set(value='on')
        elif self.last_hd_state == 'on':
            self.hdvar.set(value='off')

        self.last_hd_state = self.hdvar.get()
        self.filterchanged()

    def hichanged(self):
        if self.last_hi_state == 'off':
            self.hivar.set(value='dontcare')
            self.check_hi.state(['alternate'])
        elif self.last_hi_state == 'dontcare':
            self.hivar.set(value='on')
        elif self.last_hi_state == 'on':
            self.hivar.set(value='off')

        self.last_hi_state = self.hivar.get()
        self.filterchanged()

    def corchanged(self):
        if self.last_cor_state == 'off':
            self.corvar.set(value='dontcare')
            self.check_cor.state(['alternate'])
        elif self.last_cor_state == 'dontcare':
            self.corvar.set(value='on')
        elif self.last_cor_state == 'on':
            self.corvar.set(value='off')

        self.last_cor_state = self.corvar.get()
        self.filterchanged()

    def dropdownchanged(self, language):
        self.dropdownvar.set(language)
        self.filterchanged()

    def filterchanged(self):
        for (season, dataset) in self.dataset.items():

            # clear the season tree
            self.trees[season].delete(*self.trees[season].get_children())

            for episodesub in dataset:

                languageshow = False
                if self.dropdownvar.get() == "All languages":
                    languageshow = True
                elif self.dropdownvar.get() == episodesub['language']:
                    languageshow = True

                hdshow = False
                if self.hdvar.get() == 'dontcare':
                    hdshow = True
                elif episodesub['hd'] == True and self.hdvar.get() == 'on':
                    hdshow = True
                elif episodesub['hd'] == False and self.hdvar.get() == 'off':
                    hdshow = True

                hishow = False
                if self.hivar.get() == 'dontcare':
                    hishow = True
                elif episodesub['hi'] == True and self.hivar.get() == 'on':
                    hishow = True
                elif episodesub['hi'] == False and self.hivar.get() == 'off':
                    hishow = True

                corshow = False
                if self.corvar.get() == 'dontcare':
                    corshow = True
                elif episodesub['corrected'] == True and self.corvar.get() == 'on':
                    corshow = True
                elif episodesub['corrected'] == False and self.corvar.get() == 'off':
                    corshow = True

                if hdshow and hishow and corshow and languageshow:
                    # convert the dict to a list
                    data = []
                    for label in SubtitleSelectionPage.dataset_labels:
                        data.append(episodesub[label])

                    # add the list to the tree
                    self.trees[season].insert('', 'end', values=data)
