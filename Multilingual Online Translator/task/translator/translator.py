"""
Local translator with remote translating.
"""

import argparse
import sys

import requests
from bs4 import BeautifulSoup

# speed up download
s = requests.Session()


class Translator:
    LANGS = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew',
             'japanese', 'dutch', 'polish', 'portuguese', 'romanian',
             'russian', 'turkish']
    ADDRESS = 'https://context.reverso.net/translation'

    source_lang: int = None
    target_lang: int = None
    word: str
    translation_board: list = []
    translations: list
    examples: zip
    translations_board = {}

    def __init__(self):
        print(*[
            'Hello, welcome to the translator. Translator supports:',
            *[f'{i + 1}. {L.capitalize()}' for i, L in enumerate(self.LANGS)]
        ], sep='\n')

    def direction(self, target_lang: str = None):
        if target_lang is None:
            target_lang = self.target_lang
        return f'{self.LANGS[self.source_lang]}-{target_lang}'

    def translate(self, source: int, target: int, word: str):
        self.source_lang = source - 1
        self.target_lang = target - 1
        self.word = word

        if self.target_lang < 0:
            for t_lang_id, t_lang in enumerate(self.LANGS):
                if t_lang_id == self.source_lang:
                    continue
                self.translate_online(t_lang, word)
        else:
            target_language = self.LANGS[self.target_lang]
            self.translate_online(target_language, word)

        # store translations to file
        self.store_translation()

        # print.report
        self.report()

    def prepare_recipe(self):
        dishes_count = len(self.translations_board.keys())
        self.translation_board = []
        i = 0
        for target, dish in self.translations_board.items():
            if target == self.LANGS[self.source_lang]:
                continue
            target_language = target.capitalize()
            nl = "" if i == 0 else "\n"
            self.translation_board.append(
                f'\n{nl}{target_language} Translations:')
            t = dish['translations']
            translations = [t[0]] if dishes_count > 1 else t

            for t in translations:
                self.translation_board.append(f'{t}')

            self.translation_board.append(f'\n{target_language} Examples:')

            e = dish['examples']
            dish_examples = [list(e)[0]] if dishes_count > 1 else e
            examples = ['\n'.join(e) for e in dish_examples]

            for t in examples:
                self.translation_board.append(f'{t}')
            i = i + 1

    def store_translation(self):
        file_name = f'{self.word}.txt'

        with open(file_name, 'w') as file:
            lines = [f'{r}\n' for rcp in self.translation_board for r in rcp]
            file.writelines(lines)
            print(f'File "{file_name}" saved.', file=sys.stderr)

    def translate_online(self, target: str, word: str):
        target_lang = target.capitalize()
        url = f'{self.ADDRESS}/{self.direction(target)}/{word}'
        print(f'Request for {target_lang} translation to: {url}')

        r = s.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(f'{r.status_code} {r.reason}')

        if r.ok:
            """Prepare translation board"""

            # parse response
            soup = BeautifulSoup(r.content, 'html.parser')
            # parse translations
            self.translations = [
                t.text for i, t in
                enumerate(soup.find_all('span', {'class': 'display-term'}))
            ]
            # parse examples
            source_soup = soup.find_all('div', {'class': 'src'})
            target_soup = soup.find_all('div', {'class': 'trg'})
            # zip (pair) examples for use later
            self.examples = zip(
                [e.text.strip() for e in source_soup if e.text.strip()],
                [e.text.strip() for e in target_soup if e.text.strip()]
            )

            # Complete the dish for dinner
            dish = {
                'translations': self.translations,
                'examples': self.examples,
            }

            def prepare_lang_translation(source_lang, translations_count):
                if target == source_lang:
                    # skip translation to source_lang
                    return None

                recipe = []
                target_language = target.capitalize()

                recipe.append(f'{target_language} Translations:')
                t = dish['translations']
                translations = [t[0]] if translations_count > 1 else t
                recipe += translations

                recipe.extend(['', f'{target_language} Examples:'])

                e = dish['examples']
                # get all examples or just first if target_lang was `0`
                ex = [list(e)[0]] if translations_count > 1 else list(e)
                # flatten the array with examples pairs
                recipe.extend([rcp for tr in ex for rcp in list(tr) + ['']])
                # add new line between different languages translations
                recipe.extend([''])

                return recipe

            single_translation = prepare_lang_translation(
                self.LANGS[self.source_lang],
                len(self.translations_board.keys())
            )
            if single_translation:
                self.translation_board.append(single_translation)

            self.translations_board[target] = dish

    def report(self):
        dishes_count = len(self.translations_board.keys())
        print(
            f'There is translations board with {dishes_count} languages!',
            file=sys.stderr
        )
        for line in self.translation_board:
            print(*line, sep='\n')


"""
Pass `-t` to the command that starts the program for local tests
"""
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')
if parser.parse_args().test:
    Translator().translate(3, 4, 'hello')
    Translator().translate(3, 0, 'hello')
    Translator().translate(12, 3, 'глаза')
    exit('Enjoy your meal!')

Translator().translate(
    int(input("Type the number of your language:\n")),
    int(input(
        "Type the number of a language you want to translate to"
        " or '0' to translate to all languages:\n"
    )),
    input("Type the word you want to translate:\n")
)
