import tkinter as tk
from tkinter import ttk
from fetchandparse import FetchAndParse
from tkinter.font import Font
import selectshowpage

__author__ = 'Anders'

class SubtitleSelectionPage(tk.Frame):
    label1 = None
    notebook = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        SubtitleSelectionPage.label1 = ttk.Label(self, text="Unknown show")

        button1 = ttk.Button(self, text="Go to page one",
                             command=lambda: controller.show_frame(selectshowpage.SelectShowPage))



        SubtitleSelectionPage.notebook = ttk.Notebook(self)

        SubtitleSelectionPage.label1.grid(row=0, column=0)
        SubtitleSelectionPage.notebook.grid(row=1, column=0, sticky='nsew')
        button1.grid(row=2, column=0)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_rowconfigure(self, 1, weight=1)

    def updatedisplay(self, selectedshow):
        SubtitleSelectionPage.label1.config(text=selectedshow[1])
        seasons = FetchAndParse.getseasons(self, selectedshow[0])
        columns = ('ep', 'name', 'lang', 'vers', 'completed', 'hi', 'corrected', 'hd')
        for eachseason in seasons:
            frame = ttk.Frame(SubtitleSelectionPage.notebook)
            SubtitleSelectionPage.notebook.add(frame, text="S{:02}".format(eachseason))

            tree = ttk.Treeview(frame, columns=columns, show='headings')
            tree.grid(row=0, column=0, sticky='nsew')
            tk.Grid.grid_rowconfigure(frame, 0, weight=1)
            tk.Grid.grid_columnconfigure(frame, 0, weight=1)

            for c in columns:
                tree.heading(c, text=c.title())
                tree.column(c, width=Font().measure(c.title()))

            dataset = FetchAndParse.getsubtitlelist(self, selectedshow[0], eachseason)
            dataset_labels = ['episode', 'name', 'language', 'versions', 'completed', 'hi', 'corrected', 'hd']
            for eachdataset in dataset:
                data = []
                for label in dataset_labels:
                    data.append(eachdataset[label])
                tree.insert('', 'end', values=data)

