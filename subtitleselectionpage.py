import tkinter as tk
from tkinter import ttk
from fetchandparse import FetchAndParse
from tkinter.font import Font
import selectshowpage

__author__ = 'Anders'


class SubtitleSelectionPage(tk.Frame):
    label1 = None
    notebook = None

    def filterchanged(self):
        print(self.hivar.get())
        print(self.hdvar.get())
        print(self.corvar.get())

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        SubtitleSelectionPage.label1 = ttk.Label(self, text="Unknown show")

        button1 = ttk.Button(self, text="Go to page one",
                             command=lambda: controller.show_frame(selectshowpage.SelectShowPage))

        SubtitleSelectionPage.notebook = ttk.Notebook(self)

        self.hivar = tk.BooleanVar(self)
        self.hdvar = tk.BooleanVar(self)
        self.corvar = tk.BooleanVar(self)

        check_hi = ttk.Checkbutton(self, text="HI", variable=self.hivar, command=self.filterchanged)
        check_hd = ttk.Checkbutton(self, text="HD", variable=self.hdvar, command=self.filterchanged)
        check_cor = ttk.Checkbutton(self, text="Corrected", variable=self.corvar, command=self.filterchanged)

        dropdownvar = tk.StringVar(self)
        dropdownvar.set("one") # default value
        dropdown = ttk.OptionMenu(self, dropdownvar, "one", "two", "three")

        SubtitleSelectionPage.label1.grid(row=0, column=0, columnspan=4)
        SubtitleSelectionPage.notebook.grid(row=1, column=0, columnspan=4, sticky='nsew')

        check_hi.grid(row=2, column=0)
        check_hd.grid(row=2, column=1)
        check_cor.grid(row=2, column=2)
        dropdown.grid(row=2, column=3)

        button1.grid(row=3, column=0)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_columnconfigure(self, 1, weight=1)
        tk.Grid.grid_columnconfigure(self, 2, weight=1)
        tk.Grid.grid_columnconfigure(self, 3, weight=1)
        tk.Grid.grid_rowconfigure(self, 1, weight=1)


    def updatedisplay(self, selectedshow):
        SubtitleSelectionPage.label1.config(text=selectedshow[1])
        seasons = FetchAndParse.getseasons(selectedshow[0])
        columns = ('ep', 'name', 'lang', 'vers', 'completed', 'hi', 'corrected', 'hd')

        # make sure there's no tabs displayed
        for tab in SubtitleSelectionPage.notebook.tabs():
            SubtitleSelectionPage.notebook.forget(tab)

        for eachseason in seasons:
            frame = ttk.Frame(SubtitleSelectionPage.notebook) # use the notebook frame
            SubtitleSelectionPage.notebook.add(frame, text="S{:02}".format(eachseason))

            tree = ttk.Treeview(frame, columns=columns, show='headings')
            tree.grid(row=0, column=0, sticky='nsew')
            tk.Grid.grid_rowconfigure(frame, 0, weight=1)
            tk.Grid.grid_columnconfigure(frame, 0, weight=1)

            for column in columns:
                tree.heading(column, text=column.title())
                tree.column(column, width=Font().measure(column.title()))

            dataset = FetchAndParse.getsubtitlelist(selectedshow[0], eachseason)
            dataset_labels = ['episode', 'name', 'language', 'versions', 'completed', 'hi', 'corrected', 'hd']
            for eachdataset in dataset:
                data = []
                for label in dataset_labels:
                    data.append(eachdataset[label])
                tree.insert('', 'end', values=data)
