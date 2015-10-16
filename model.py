from fetchandparse import FetchAndParse
from fnmatch import fnmatch
from subtitleselectionpage import SubtitleSelectionPage

import login

__author__ = 'Anders'


class Model:

    def __init__(self, view):
        self.fetchandparser = FetchAndParse()
        self.view = view

        self.shows = self.fetchandparser.getshows()
        self.seasons = None
        self.subtitles = None

        # fill up the shows list
        self.updateshowlist('*')

    def _indextoshow(self, index):
        return self.filteredshows[index]

    def displayshow(self, showtodisplay):
        show = self._indextoshow(showtodisplay)
        self.view.frames[SubtitleSelectionPage].label.set(show[1])
        self.seasons = self.fetchandparser.getseasons(show[0])

        self.subtitles = {}  # clear the subtitles list, if the back button was used

        # Remove all season tabs, so we start on a clean slate
        for tab in self.view.frames[SubtitleSelectionPage].notebook.tabs():
            SubtitleSelectionPage.notebook.forget(tab)

        for season in self.seasons:


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
