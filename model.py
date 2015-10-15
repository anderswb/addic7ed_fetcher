from fetchandparse import FetchAndParse
from fnmatch import fnmatch

__author__ = 'Anders'


class Model:

    def __init__(self, view):
        self.fetchandparser = FetchAndParse()
        self.view = view

        self.shows = self.fetchandparser.getshows()
        self.seasons = None

        # fill up the shows list
        self.updateshowlist('*')

    def _indextoshow(self, index):
        return self.filteredshows[index]

    def displayshow(self, showtodisplay):
        print(self._indextoshow(showtodisplay))

    def updateshowlist(self, filterstring):
        self.view.clearshows()
        self.filteredshows = []
        for show in self.shows:
            if fnmatch(show[1].lower(), filterstring.lower()):
                self.view.addshow(show[1])
                self.filteredshows.append(show)

