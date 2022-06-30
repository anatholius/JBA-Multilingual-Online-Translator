import requests

from bs4 import BeautifulSoup

# Possibly misspelled word: `misspelt`
print(BeautifulSoup(requests.get(input()).text, 'html.parser').h1.text)
