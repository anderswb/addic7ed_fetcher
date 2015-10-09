from lxml import html
import requests

__author__ = 'Anders'


class fetchAndParse:

    def getshows(self):
        """
        Get the list of shows available from the main page of addic7ed
        :return: A list of tuple with the first entry being the addic7ed given value of the show,
        and the second entry being the name of the show.
        """
        page = requests.get('http://www.addic7ed.com')
        tree = html.fromstring(page.text)

        show_values = tree.xpath('//select[@id="qsShow"]/option/@value')
        show_names = tree.xpath('//select[@id="qsShow"]/option/text()')

        shows = []
        for i, value in enumerate(show_values):
            if value != '0':
                shows.append((value, show_names[i]))

        shows.sort(key=lambda tup: tup[1], reverse=True)
        return shows

    def getseasons(self, showvalue):
        page = requests.get('http://www.addic7ed.com/show/{}'.format(showvalue))
        tree = html.fromstring(page.text)

        # get the text on the buttons inside the s1 div
        seasons_str = tree.xpath('//div[@id="sl"]/button/text()')
        seasons = []
        for season in seasons_str:
            seasons.append(int(season))

        return seasons

    def getsubtitlelist(self, showvalue, season):
        page = requests.get('http://www.addic7ed.com/ajax_loadShow.php?show={}&season={}'.format(showvalue, season))
        tree = html.fromstring(page.text)

        seasons = tree.xpath('//div[@id="season"]/table/tbody/tr/td[1]/text()')
        episodes = tree.xpath('//div[@id="season"]/table/tbody/tr/td[2]/text()')
        names = tree.xpath('//div[@id="season"]/table/tbody/tr/td[3]/a/text()')
        languages = tree.xpath('//div[@id="season"]/table/tbody/tr/td[4]/text()')
        versions = tree.xpath('//div[@id="season"]/table/tbody/tr/td[5]')
        completed = tree.xpath('//div[@id="season"]/table/tbody/tr/td[6]')
        hi = tree.xpath('//div[@id="season"]/table/tbody/tr/td[7]')
        corrected = tree.xpath('//div[@id="season"]/table/tbody/tr/td[8]')
        hd = tree.xpath('//div[@id="season"]/table/tbody/tr/td[9]')
        dl_links = tree.xpath('//div[@id="season"]/table/tbody/tr/td[10]/a/@href')

        for i in range(0, len(seasons)):
            if hd[i].text == '\u2714':
                hd[i] = True
            else:
                hd[i] = False

            if corrected[i].text == '\u2714':
                corrected[i] = True
            else:
                corrected[i] = False

            if versions[i].text is None:
                versions[i] = ''
            else:
                versions[i] = versions[i].text

            if completed[i].text == "Completed":
                completed[i] = True
            else:
                completed[i] = False

            if hi[i].text == '\u2714':
                hi[i] = True
            else:
                hi[i] = False

        episodelist = []
        for i in range(0, len(seasons)):
            episodelist.append({'season': seasons[i],
                                'episode': episodes[i],
                                'name': names[i],
                                'language': languages[i],
                                'versions': versions[i],
                                'completed': completed[i],
                                'hi': hi[i],
                                'corrected': corrected[i],
                                'hd': hd[i],
                                'dl link': dl_links[i]})
        return episodelist


if __name__ == "__main__":
    fetchandparser = fetchAndParse()
    shows = fetchandparser.getshows()
    print('Found {} shows'.format(len(shows)))

    trueblood_seasons = fetchandparser.getseasons(366)
    print("Found {} seasons in the True Blood show:".format(len(trueblood_seasons)))
    print(trueblood_seasons)

    sublist = fetchandparser.getsubtitlelist(366, 1)
    print('Found {} subtitles in season 1 of True Blood'.format(len(sublist)))


