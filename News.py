from bs4 import BeautifulSoup
import requests


def GetNews():
    # Requesting the url
    res = requests.get('https://www.bing.com/news/search?q=World')

    soup = BeautifulSoup(res.text, 'html.parser')  # Defining bs4 object

    allNews_html = soup.find_all("div", class_='t_t')
    allNews = []

    for tag in allNews_html:
        title = tag.find("a", class_='title').text
        link = tag.find("a", class_='title').get('href')

        if title and link:
            allNews.append([title, link])

    return allNews


TITLES = []
LINKS = []

for eachNews in GetNews():
    TITLES.append(eachNews[0])
    LINKS.append(eachNews[1])
    print(TITLES)
    print(LINKS)
