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

if __name__ == "__main__":
    fetchandparser = fetchAndParse()
    print(fetchandparser.getshows())
