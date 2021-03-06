import requests
from bs4 import BeautifulSoup
import datetime


def RequestURL():
    res = requests.get('https://weather.com/en-IN/weather/today/')
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def GetWeather():
    '''
    Weather Calculation
    '''
    soup = RequestURL()

    currentWeather = soup.find(
        'span', class_='CurrentConditions--tempValue--3KcTQ').text

    typeWeather = soup.find(
        'div', class_='CurrentConditions--phraseValue--2xXSr').text

    return currentWeather, typeWeather


def GetDate():
    now = datetime.datetime.now()
    day = now.strftime('%a')
    date = now.strftime('%d %b')
    return day, date
