"""
Local translator.
"""

import argparse

import requests
from bs4 import BeautifulSoup

langs = {
    'fr': 'french',
    'en': 'english',
}
dirs = {
    'fr': f'{langs["en"]}-{langs["fr"]}',
    'en': f'{langs["fr"]}-{langs["en"]}',
}


def translate(target_lang: str, word: str):
    """
    There are lies!
    There in the description of the stage.

    Limiting the examples to 5 spoils tests!
    """

    print(f'You chose "{target_lang}" as a language to translate "{word}".')

    url = f'https://context.reverso.net/translation/{dirs[target_lang]}/{word}'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'{r.status_code} {r.reason}')

    if r.ok:
        # cook the pizza, ee.. soup
        soup = BeautifulSoup(r.content, 'html.parser')
        translations = [t.text for i, t in enumerate(soup.find_all('span', {
            'class': 'display-term'
        }))]

        # cook examples translation soups
        source_soup = soup.find_all('div', {'class': 'src ltr'})
        target_soup = soup.find_all('div', {'class': 'trg ltr'})
        # prepare examples translation pairs with stripping values texts
        examples = zip(
            [e.text.strip() for e in source_soup if e.text.strip()],
            [e.text.strip() for e in target_soup if e.text.strip()]
        )

        # Bring your meal to the table, dinner!
        print(f'\n{langs[target_lang].capitalize()} Translations:')
        print(*translations, sep='\n')
        print(f'\n{langs[target_lang].capitalize()} Examples:')
        print(*['\n'.join(e) for e in examples], sep='\n\n')


"""
Pass -t for local tests to run program
"""
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')
if parser.parse_args().test:
    translate('fr', 'hello')
    exit('Thanks for testing!')

lang = input(
    'Type "en" if you want to translate from French into English, or "fr" if '
    'you want to translate from English into French:\n'
)
word = input('Type the word you want to translate:\n')
translate(lang, word)
