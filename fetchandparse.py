from lxml import html
import requests

__author__ = 'Anders'


class fetchAndParse:

    def getshows(self):
        """
        Get the list of shows available from the main page of addic7ed
        :return: A dict with the key being the addic7ed given value of the show, and the value being the name of
        the show.
        """
        page = requests.get('http://www.addic7ed.com')
        tree = html.fromstring(page.text)

        show_values = tree.xpath('//select[@id="qsShow"]/option/@value')
        show_names = tree.xpath('//select[@id="qsShow"]/option/text()')

        shows = {}
        for i, value in enumerate(show_values):
            if value != '0':
                shows[int(value)] = show_names[i]

        return shows

    def getseasons(self, showvalue):
        page = requests.get('http://www.addic7ed.com/show/{}'.format(showvalue))
        tree = html.fromstring(page.text)

        # get the text on the buttons inside the s1 div
        seasons = tree.xpath('//div[@id="sl"]/button/text()')
        return seasons

if __name__ == "__main__":
    fetchandparser = fetchAndParse()
    shows = fetchandparser.getshows()
    print('Found {} shows'.format(len(shows)))

    trueblood_seasons = fetchandparser.getseasons(366)
    print("Found {} seasons in the True Blood show:".format(len(trueblood_seasons)))
    print(trueblood_seasons)


