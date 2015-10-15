from fetchandparse import FetchAndParse

__author__ = 'Anders'


class Model:

    def __init__(self):
        self.fetchandparser = FetchAndParse()

        self.shows = None
        self.seasons = None


    def get_shows(self):
        if self.shows is None:
            self.shows = self.fetchandparser.getshows()

        return self.shows

    def indextoshow(self, index):
        return self.shows[index]