import requests

from bs4 import BeautifulSoup

letter = 'S'
url = input()

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
print([
    a.text
    for a in soup.find_all('a')
    if (
        len(a.text) > 1
        and a.text.startswith(letter)
        and (
            'topics' in a.get("href")
            or 'entity' in a.get("href")
        )
    )
])
