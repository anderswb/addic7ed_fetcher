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

__author__ = 'Anders'


class SubtitleSelectionPage(tk.Frame):
    label1 = None
    notebook = None
    dataset_labels = ['episode', 'name', 'language', 'versions', 'completed', 'hi', 'corrected', 'hd']

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.container = controller
        self.trees = {}
        self.displayedsubs = {}
        self.dataset = {}

        SubtitleSelectionPage.label1 = ttk.Label(self, text="Unknown show")

        button_back = ttk.Button(self, text="Back",
                                 command=lambda: controller.show_frame(selectshowpage.SelectShowPage))
        button_ok = ttk.Button(self, text="OK",
                               command=lambda: self.downloadsubs())

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

        # remove all tabs
        for tab in SubtitleSelectionPage.notebook.tabs():
            SubtitleSelectionPage.notebook.forget(tab)

        ## TODO: forget treeviews as well

        # populate the dataset
        self.dataset = {}  # clear out old data
        for eachseason in seasons:
            frame = ttk.Frame(SubtitleSelectionPage.notebook)  # use the notebook frame
            SubtitleSelectionPage.notebook.add(frame, text="S{:02}".format(eachseason))  # add new tab

            # Create a treeview for the current season, and add it to the tab
            self.trees[eachseason] = ttk.Treeview(frame, columns=columns, show='headings')
            self.trees[eachseason].grid(row=0, column=0, sticky='nsew')

            # Create y scrollbar
            ysb = ttk.Scrollbar(frame, orient='vertical', command=self.trees[eachseason].yview)
            self.trees[eachseason].configure(yscroll=ysb.set)
            ysb.grid(row=0, column=1, sticky='ns')

            tk.Grid.grid_rowconfigure(frame, 0, weight=1)
            tk.Grid.grid_columnconfigure(frame, 0, weight=1)

            # Put in the headings on the new treeview
            for column in columns:
                self.trees[eachseason].heading(column, text=column.title())
                self.trees[eachseason].column(column, width=Font().measure(column.title()))

            # Fetch the dataset for the current season
            self.dataset[eachseason] = FetchAndParse.getsubtitlelist(selectshowpage.SelectShowPage.selectedshow[0],
                                                                     eachseason)

            self.trees[eachseason].tag_configure('white', background='white')
            self.trees[eachseason].tag_configure('gray', background='lightgray')

        self.filterchanged()  # update the tree view with the subtitles stored in self.dataset

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
        self.last_hd_state = self.checkboxchange(self.last_hd_state, self.hdvar, self.check_hd)
        self.filterchanged()

    def hichanged(self):
        self.last_hi_state = self.checkboxchange(self.last_hi_state, self.hivar, self.check_hi)
        self.filterchanged()

    def corchanged(self):
        self.last_cor_state = self.checkboxchange(self.last_cor_state, self.corvar, self.check_cor)
        self.filterchanged()

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

    def dropdownchanged(self, language):
        self.dropdownvar.set(language)
        self.filterchanged()

    def filterchanged(self):
        self.displayedsubs = {}
        for (season, dataset) in self.dataset.items():

            # clear the season tree
            self.trees[season].delete(*self.trees[season].get_children())

            self.displayedsubs[season] = []

            colortag = 'white'
            last_episode = None
            for episodesub in dataset:

                languageshow = self.dropdownvar.get() == "All languages" or \
                               self.dropdownvar.get() == episodesub['language']

                hdshow = self.hdvar.get() == 'dontcare' or \
                    (episodesub['hd'] == True and self.hdvar.get() == 'on') or \
                    (episodesub['hd'] == False and self.hdvar.get() == 'off')

                hishow = self.hivar.get() == 'dontcare' or \
                    (episodesub['hi'] == True and self.hivar.get() == 'on') or \
                    (episodesub['hi'] == False and self.hivar.get() == 'off')

                corshow = self.corvar.get() == 'dontcare' or \
                    (episodesub['corrected'] == True and self.corvar.get() == 'on') or \
                    (episodesub['corrected'] == False and self.corvar.get() == 'off')

                # if all of the filter conditions are true
                if hdshow and hishow and corshow and languageshow:
                    # convert the dict to a list
                    data = []
                    for label in SubtitleSelectionPage.dataset_labels:
                        data.append(episodesub[label])

                    # Find the colortag for the current row
                    if episodesub['episode'] != last_episode and last_episode is not None:
                        if colortag == 'white':
                            colortag = 'gray'
                        else:
                            colortag = 'white'
                    last_episode = episodesub['episode']

                    # add the list to the tree
                    self.trees[season].insert('', 'end', values=data, tags = (colortag,))

                    # add the dataset to the list of displayed subs, making it easier to download them later on
                    self.displayedsubs[season].append(episodesub)

    def downloadsubs(self):
        showstodownload = []
        urllist = []
        for (season, seasontree) in self.trees.items():
            for selection in seasontree.selection():
                selection_index = seasontree.index(selection)
                selected_dataset = self.displayedsubs[season][selection_index]
                showstodownload.append(selected_dataset)
                urllist.append('http://www.addic7ed.com' + selected_dataset['dl link'])

        thread1 = Thread(target=self.downloadandsave, args=(showstodownload, ))
        thread1.start()
        DownloadDialog(self, showstodownload)
        thread1.join()

    def downloadandsave(self, urllist):
        for idx, url in enumerate(urllist):
            while DownloadDialog.statustree is None:
                time.sleep(1)
            DownloadDialog.updateprogress(idx, 'Downloading')
            time.sleep(1)
            DownloadDialog.updateprogress(idx, 'Done')

        # request = session.get(url)
        # content = request.content  # get the file content
        #
        # if content[0:8] == b'<!DOCTYP':
        #     messagebox.showerror('Download limit', 'Daily download count exceeded.')
        #     return False
        # else:
        #     # get the filename from the header
        #     headers = request.headers
        #     if 'Content-Disposition' in headers:  # check if a filename was included
        #         content_disp = headers['Content-Disposition']
        #         filename = findall(r'filename="(.+)"', content_disp)[0]
        #
        #         # Save the file content
        #         with open(filename, 'wb') as fp:
        #             fp.write(content)
        #         return True
        #     else:
        #         messagebox.showerror('Download error', 'Can\'t download subtitle, '
        #                                                'it is probably not complete.')
        #         return False
