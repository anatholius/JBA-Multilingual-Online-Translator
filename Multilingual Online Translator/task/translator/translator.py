"""
Local translator with remote translating.
"""

import argparse

import requests
from bs4 import BeautifulSoup


class Translator:
    LANGS = [
        'arabic',
        'german',
        'english',
        'spanish',
        'french',
        'hebrew',
        'japanese',
        'dutch',
        'polish',
        'portuguese',
        'romanian',
        'russian',
        'turkish',
    ]
    source_lang: int = None
    target_lang: int = None

    def __init__(self):
        print(*[
            'Hello, welcome to the translator. Translator supports:',
            *[f'{i + 1}. {L.capitalize()}' for i, L in enumerate(self.LANGS)]
        ], sep='\n')

    def direction(self):
        return f'{self.LANGS[self.source_lang]}-{self.LANGS[self.target_lang]}'

    def translate(self, source: int, target: int, word: str):
        self.source_lang = source - 1
        self.target_lang = target - 1

        address = 'https://context.reverso.net/translation'
        url = f'{address}/{self.direction()}/{word}'
        print(f'Asking for translation to: {url}')
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(f'{r.status_code} {r.reason}')

        if r.ok:
            # Cook the pizza, ee.. soup
            soup = BeautifulSoup(r.content, 'html.parser')
            translations = [
                t.text for i, t in
                enumerate(soup.find_all('span', {'class': 'display-term'}))
            ]

            # Cook examples translation soups
            source_soup = soup.find_all('div', {'class': 'src ltr'})
            target_soup = soup.find_all('div', {'class': 'trg ltr'})
            # Prepare examples translation pairs with stripping values texts
            examples = zip(
                [e.text.strip() for e in source_soup if e.text.strip()],
                [e.text.strip() for e in target_soup if e.text.strip()]
            )

            # Bring your meal to the table, dinner!
            print(
                f'\n{self.LANGS[self.target_lang].capitalize()} Translations:')
            print(*translations, sep='\n')
            print(f'\n{self.LANGS[self.target_lang].capitalize()} Examples:')
            print(*['\n'.join(e) for e in examples], sep='\n\n')


"""
Pass -t for local tests to run program
"""
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')
if parser.parse_args().test:
    Translator().translate(3, 4, 'hello')
    exit('Thanks for testing!')

Translator().translate(
    int(input('Type the number of your language:\n')),
    int(input('Type the number of language you want to translate to:\n')),
    input('Type the word you want to translate:\n')
)
