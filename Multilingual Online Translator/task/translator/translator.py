import requests

from bs4 import BeautifulSoup

dirs = {
    'fr': 'english-french',
    'en': 'french-english',
}

lang = input(
    'Type "en" if you want to translate from French into English, or "fr" if '
    'you want to translate from English into French:\n'
)
word = input('Type the word you want to translate:\n')
print(f'You chose "{lang}" as a language to translate "{word}".')

url = f'https://context.reverso.net/translation/{dirs[lang]}/{word}'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(f'{r.status_code} {r.reason}')

if r.ok:
    print('Translations')
    soup = BeautifulSoup(r.content, 'html.parser')
    print([t.text for t in soup.find_all('span', {'class': 'display-term'})])
    print([
        t.text.strip()
        for t in soup.find_all('div', {'class': 'ltr'})
        if t.text.strip() != ''
    ])
