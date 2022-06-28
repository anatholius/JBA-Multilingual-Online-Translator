import requests

from bs4 import BeautifulSoup


def find_paragraph(word: str, url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print([p.text for p in soup.find_all('p') if word in p.text][0])


find_paragraph(input(), input())
