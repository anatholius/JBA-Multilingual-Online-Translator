import requests

from bs4 import BeautifulSoup


def find_subtitle(index: int, url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    res = soup.find_all('h2')[index]
    print(res.text)


find_subtitle(int(input()), input())
