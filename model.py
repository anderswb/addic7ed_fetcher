from fetchandparse import FetchAndParse
from fnmatch import fnmatch
from pages.subtitleselectionpage import SubtitleSelectionPage
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

import login

__author__ = 'Anders'


class Model:

    def __init__(self, view):
        self.fetchandparser = FetchAndParse()
        self.view = view

        self.shows = self.fetchandparser.getshows()
        self.seasons = None
        self.subtitles = None
        self.subtitletrees = {}
        self.displayedsubs = {}

        # fill up the shows list
        self.updateshowlist('*')

    def _indextoshow(self, index):
        return self.filteredshows[index]

    def displayshow(self, showtodisplay):
        show = self._indextoshow(showtodisplay)
        page = self.view.frames[SubtitleSelectionPage]
        page.label.set(show[1])
        self.seasons = self.fetchandparser.getseasons(show[0])

        self.subtitles = {}  # clear the subtitles list, if the back button was used

        # Remove all season tabs, so we start on a clean slate
        for tab in page.notebook.tabs():
            SubtitleSelectionPage.notebook.forget(tab)

        columns = ('ep', 'name', 'lang', 'vers', 'completed', 'hi', 'corrected', 'hd')
        # TODO: Move some of this stuff to the view
        for season in self.seasons:
            # Fetch the available for the current season
            self.subtitles[season] = self.fetchandparser.getsubtitlelist(show[0], season)

            frame = ttk.Frame(page.notebook)  # use the notebook frame

            # add new tab, with the name of the season
            page.notebook.add(frame, text="S{:02}".format(season))

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
                tree.column(column, width=Font().measure(column.title()))

            # configure the tags used for alternating the colors of the rows
            tree.tag_configure('white', background='white')
            tree.tag_configure('gray', background='lightgray')

            self.subtitletrees[season] = tree  # store the tree for later use

        # Populate languages filter dropdown menu
        languages = self.fetchandparser.getlanguages(self.subtitles)
        menu = page.filterpanel.dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All languages",
                         command=lambda value="All languages":
                         page.filterpanel.language_dropdownchanged(value))
        for language in languages:
            menu.add_command(label=language,
                             command=lambda value=language:
                             page.filterpanel.language_dropdownchanged(value))

        self.updatesubtitlelist('All languages', 'dontcare', 'dontcare', 'dontcare')

    def language_dropdownchanged(self, language):
        print(language)

    def updatesubtitlelist(self, language, hd, hi, corrected):
        print(language, hd, hi, corrected)
        self.displayedsubs = {}

        # iterate over each subtitle available for the current show
        for (season, dataset) in self.subtitles.items():
            tree = self.subtitletrees[season]

            tree.delete(*tree.get_children())  # clear the season tree
            self.displayedsubs[season] = []  # clear the list of displayed subtitles

            colortag = 'white'  # first row is always white
            last_episode = None
            for episodesub in dataset:

                languageshow = language == "All languages" or \
                               language == episodesub['language']

                hdshow = hd == 'dontcare' or \
                    (episodesub['hd'] == True and hd == 'on') or \
                    (episodesub['hd'] == False and hd == 'off')

                hishow = hi == 'dontcare' or \
                    (episodesub['hi'] == True and hi == 'on') or \
                    (episodesub['hi'] == False and hi == 'off')

                corshow = corrected == 'dontcare' or \
                    (episodesub['corrected'] == True and corrected == 'on') or \
                    (episodesub['corrected'] == False and corrected == 'off')

                # if all of the filter conditions are true
                if hdshow and hishow and corshow and languageshow:
                    # convert the dict to a list, as needed by the treeview
                    data = []
                    for label in FetchAndParse.dataset_labels:
                        data.append(episodesub[label])

                    # Find the colortag for the current row
                    if episodesub['episode'] != last_episode and last_episode is not None:
                        if colortag == 'white':
                            colortag = 'gray'
                        else:
                            colortag = 'white'
                    last_episode = episodesub['episode']

                    # add the list to the tree
                    tree.insert('', 'end', values=data, tags = (colortag,))

                    # add the dataset to the list of displayed subs, making it easier to download them later on
                    self.displayedsubs[season].append(episodesub)

    def updateshowlist(self, filterstring):
        self.view.clearshows()
        self.filteredshows = []
        for show in self.shows:
            if fnmatch(show[1].lower(), filterstring.lower()):
                self.view.addshow(show[1])
                self.filteredshows.append(show)

    def updatetitle(self):
        user = login.get_current_user()
        if user is not None:
            title = "Addic7ed Fetcher - logged in as: {}".format(user)
        else:
            title = "Addic7ed Fetcher - not logged in"
        self.view.settitle(title)

    def login(self, username, password):
        login.login(username, password)
