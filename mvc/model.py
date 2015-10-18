from webpageaccess.fetchandparse import FetchAndParse as FetchAndParse
from fnmatch import fnmatch
from pages.subtitleselectionpage import SubtitleSelectionPage
from pages.downloadpage import DownloadPage as DownloadPage
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import time
import re
from os import path
from os import makedirs

import webpageaccess.login as login

from webpageaccess.downloadsession import Session as Session

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
        self.substodownload = []

        self.cancel = False

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
            page.notebook.forget(tab)

        for season in self.seasons:
            # Fetch the available for the current season
            self.subtitles[season] = self.fetchandparser.getsubtitlelist(show[0], season)
            tree = self.view.frames[SubtitleSelectionPage].addtab(season)  # add a new tab with a treeview
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

        self.updateallsubtitlelists()

    def clearalldisplayedsubs(self):
        self.displayedsubs = {}  # clear the list of displayed subtitles
        for season in self.subtitles:
            tree = self.subtitletrees[season]
            tree.delete(*tree.get_children())  # clear the season tree

    def updateallsubtitlelists(self):
        self.clearalldisplayedsubs()
        for (season, dataset) in self.subtitles.items():
            page = self.view.frames[SubtitleSelectionPage]
            corrected = page.filterpanel.corrected.get()
            hi = page.filterpanel.hi.get()
            hd = page.filterpanel.hd.get()
            language = page.filterpanel.language.get()
            self.updateseasonsubtitlelist(season, dataset, language, hd, hi, corrected)

    def updateseasonsubtitlelist(self, season, seasondataset, language, hd, hi, corrected):
        tree = self.subtitletrees[season]

        colortag = 'white'  # first row is always white
        last_episode = None

        self.displayedsubs[season] = []
        # loop through all of the available subs in the season
        for episodesub in seasondataset:

            # if all of the filter conditions are true
            if self.displaysubtitle(episodesub, corrected, hd, hi, language):
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

    def displaysubtitle(self, episode_dataset, corrected, hd, hi, language):
        languageshow = language == "All languages" or \
                       language == episode_dataset['language']
        hdshow = hd == 'dontcare' or \
                 (episode_dataset['hd'] == True and hd == 'on') or \
                 (episode_dataset['hd'] == False and hd == 'off')
        hishow = hi == 'dontcare' or \
                 (episode_dataset['hi'] == True and hi == 'on') or \
                 (episode_dataset['hi'] == False and hi == 'off')
        corshow = corrected == 'dontcare' or \
                  (episode_dataset['corrected'] == True and corrected == 'on') or \
                  (episode_dataset['corrected'] == False and corrected == 'off')

        return corshow and  hdshow and hishow and languageshow

    def updatesubtitlelist(self, language, hd, hi, corrected):
        self.displayedsubs = {}

        # iterate over each subtitle available for the current show
        for (season, dataset) in self.subtitles.items():
            tree = self.subtitletrees[season]

            tree.delete(*tree.get_children())  # clear the season tree
            self.displayedsubs[season] = []  # clear the list of displayed subtitles

            colortag = 'white'  # first row is always white
            last_episode = None
            for episodesub in dataset:

                corshow, hdshow, hishow, languageshow = self.displaysubtitle(episodesub, corrected, hd, hi, language)

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

    def add_downloads(self):
        self.substodownload = []

        # clear the download list
        page = self.view.frames[DownloadPage]
        page.statustree.delete(*page.statustree.get_children())

        # find all selections in all trees
        for (season, seasontree) in self.subtitletrees.items():
            for selection in seasontree.selection():

                # for all selections:
                selection_index = seasontree.index(selection)  # get selection
                selected_dataset = self.displayedsubs[season][selection_index]  # get dataset matching the selection
                self.substodownload.append(selected_dataset)  # append the dataset to the list of subs to download

        for sub in self.substodownload:
            self.view.add_downloaditem('Pending', sub['season'], sub['episode'], 'white')

    def downloadandsave(self):
        session = Session()
        for idx, sub in enumerate(self.substodownload):
            self.view.change_downloaditemstatus(idx, 'Downloading', 'yellow')

            request = session.get(sub['dl link'])
            content = request.content  # get the file content

            success = True
            if content[0:9] == b'<!DOCTYPE':  # check if the received data was a html file instead of a sub
                htmlstring = content.decode("utf-8")
                if re.findall(r'download limit', htmlstring):
                    #messagebox.showerror('Download limit', 'Daily download count exceeded.')
                    print('Download limit')
                    break

                success = False
            else:
                # get the filename from the header
                headers = request.headers
                if 'Content-Disposition' in headers:  # check if a filename was included
                    content_disp = headers['Content-Disposition']
                    dir = 'downloads'
                    filename = re.findall(r'filename="(.+)"', content_disp)[0]
                    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)  # remove any not allowed chars
                    filename = path.join(dir, filename)

                    if not path.exists(dir):
                        makedirs(dir)

                    # Save the file content
                    with open(filename, 'wb') as fp:
                        fp.write(content)
                else:
                    #messagebox.showerror('Download error', 'Can\'t download subtitle, '
                    #                                       'it is probably not complete.')
                    print('Download error')
                    success = False

            if self.cancel:
                break

            if success == True:
                self.view.change_downloaditemstatus(idx, 'Done', 'green')
            else:
                self.view.change_downloaditemstatus(idx, 'Failed', 'red')

        self.cancel = False
        self.downloaddone()

    def downloaddone(self):
        page = self.view.frames[DownloadPage]
        page.buttonpanel.buttons['OK'].configure(state=tk.ACTIVE)
        page.buttonpanel.buttons['Cancel'].configure(state=tk.DISABLED)
        page.buttonpanel.buttons['Back'].configure(state=tk.ACTIVE)

    def canceldownload(self):
        self.cancel = True
        page = self.view.frames[DownloadPage]
        page.buttonpanel.buttons['OK'].configure(state=tk.ACTIVE)
        page.buttonpanel.buttons['Cancel'].configure(state=tk.DISABLED)
        page.buttonpanel.buttons['Back'].configure(state=tk.ACTIVE)