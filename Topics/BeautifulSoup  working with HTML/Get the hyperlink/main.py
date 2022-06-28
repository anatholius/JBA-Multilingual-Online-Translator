import requests

from bs4 import BeautifulSoup


def find_act(index: int, url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    res = soup.find_all('a')[index - 1]
    print(res.get('href'))


find_act(int(input()), input())
