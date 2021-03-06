from lxml import html
import requests

__author__ = 'Anders'


class FetchAndParse:

    dataset_labels = ['episode', 'name', 'language', 'versions', 'completed', 'hi', 'corrected', 'hd']

    @staticmethod
    def getshows():
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

        shows.sort(key=lambda tup: tup[1], reverse=False)
        return shows

    @staticmethod
    def getseasons(showvalue):
        page = requests.get('http://www.addic7ed.com/show/{}'.format(showvalue))
        tree = html.fromstring(page.text)

        # get the text on the buttons inside the s1 div
        seasons_str = tree.xpath('//div[@id="sl"]/button/text()')
        seasons = []
        for season in seasons_str:
            seasons.append(int(season))

        return seasons

    @staticmethod
    def getsubtitlelist(showvalue, season):
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
                                'dl link': 'http://www.addic7ed.com' + dl_links[i]})
        return episodelist

    @staticmethod
    def getlanguages(episodes_datasets):
        languages = set()

        if isinstance(episodes_datasets, dict):  # if this is a dict of seasons containing lists of subtitles
            for (season, datasets) in episodes_datasets.items():
                for dataset in datasets:
                    languages.add(dataset['language'])
        elif isinstance(episodes_datasets, list):  # this is just a list of subtitles from a single season
            for dataset in episodes_datasets:
                languages.add(dataset['language'])
        languages = list(languages)
        languages.sort()
        return languages


if __name__ == "__main__":
    fetchedshows = FetchAndParse.getshows()
    print('Found {} shows'.format(len(fetchedshows)))

    trueblood_seasons = FetchAndParse.getseasons(366)
    print("Found {} seasons in the True Blood show:".format(len(trueblood_seasons)))
    print(trueblood_seasons)

    sublist1 = FetchAndParse.getsubtitlelist(366, 1)
    print('Found {} subtitles in season 1 of True Blood'.format(len(sublist1)))

    sublist2 = FetchAndParse.getsubtitlelist(366, 2)

    dataset = {}
    dataset[1] = sublist1
    dataset[2] = sublist2

    fetchedlanguages = FetchAndParse.getlanguages(sublist1)
    print("Found {} languages in season 1 of True Blood:".format(len(fetchedlanguages)))

    fetchedlanguages = FetchAndParse.getlanguages(sublist2)
    print("Found {} languages in season 2 of True Blood:".format(len(fetchedlanguages)))

    fetchedlanguages = FetchAndParse.getlanguages(dataset)
    print("Found {} languages in season 1 and 2 of True Blood:".format(len(fetchedlanguages)))

    print(fetchedlanguages)
