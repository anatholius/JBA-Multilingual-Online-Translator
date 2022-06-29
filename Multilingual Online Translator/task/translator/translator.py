"""
Local translator with remote translating.
"""

import argparse
import sys

import requests
from bs4 import BeautifulSoup

s = requests.Session()


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
    ADDRESS = 'https://context.reverso.net/translation'

    source_lang: int = None
    target_lang: int = None
    word: str
    dinner_recipe: list = []
    translations: list
    examples: zip
    the_dinner = {}

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
            for lang, ingredients in enumerate(self.LANGS):
                if lang == self.source_lang:
                    continue
                self.cook_the_dish(ingredients, word)

            # Remember the recipe for dinner
            # print('Remember the recipe for dinner', file=sys.stderr)
        else:
            ingredients = self.LANGS[self.target_lang]
            self.cook_the_dish(ingredients, word)
            print('')
            print(
                'REMEMBER, you need to save file for specified target lag '
                'too!!!',
                file=sys.stderr)
            print('')

        self.remember_recipe()
        # Bring your multi-dish meal to the table, and say: dinner!
        # print('dinner!', file=sys.stderr)
        self.dinner()

    def prepare_recipe(self):
        dishes_count = len(self.the_dinner.keys())
        self.dinner_recipe = []
        i = 0
        for target, dish in self.the_dinner.items():
            if target == self.LANGS[self.source_lang]:
                continue
            target_language = target.capitalize()
            nl = "" if i == 0 else "\n"
            self.dinner_recipe.append(f'\n{nl}{target_language} Translations:')
            t = dish['translations']
            translations = [t[0]] if dishes_count > 1 else t

            for t in translations:
                self.dinner_recipe.append(f'{t}')

            self.dinner_recipe.append(f'\n{target_language} Examples:')

            e = dish['examples']
            dish_examples = [list(e)[0]] if dishes_count > 1 else e
            examples = ['\n'.join(e) for e in dish_examples]

            for t in examples:
                self.dinner_recipe.append(f'{t}')
            i = i + 1

    def remember_recipe(self):
        # preparing file
        file_name = f'{self.word}.txt'
        # file_exists = os.path.exists(file_name)

        with open(file_name, 'w') as file:
            lines = [f'{r}\n' for recipe in self.dinner_recipe for r in recipe]
            file.writelines(lines)
            print(f'Saved in file: "{file_name}"', self.dinner_recipe)

        # if file_exists:
        #     print(f'File "{file_name}" was overridden.', file=sys.stderr)

    def cook_the_dish(self, target: str, word: str):
        target_lang = target.capitalize()
        url = f'{self.ADDRESS}/{self.direction(target)}/{word}'
        print(f'Request for {target_lang} translation to: {url}')

        r = s.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(f'{r.status_code} {r.reason}')

        if r.ok:
            # Cook the pizza, ee.. soup
            soup = BeautifulSoup(r.content, 'html.parser')
            self.translations = [
                t.text for i, t in
                enumerate(soup.find_all('span', {'class': 'display-term'}))
            ]
            # Cook examples translation soups
            source_soup = soup.find_all('div', {'class': 'src'})
            target_soup = soup.find_all('div', {'class': 'trg'})
            # Prepare examples translation pairs with stripping values texts
            self.examples = zip(
                [e.text.strip() for e in source_soup if e.text.strip()],
                [e.text.strip() for e in target_soup if e.text.strip()]
            )

            # Complete the dish for dinner
            dish = {
                'translations': self.translations,
                'examples': self.examples,
            }

            def prepare_dish_recipe(source_lang, dishes_count):
                if target == source_lang:
                    return None
                recipe = []
                target_language = target.capitalize()

                recipe.append(f'{target_language} Translations:')
                t = dish['translations']
                translations = [t[0]] if dishes_count > 1 else t
                recipe += translations

                recipe.extend(['', f'{target_language} Examples:'])

                e = dish['examples']
                examples = [list(e)[0]] if dishes_count > 1 else list(e)
                recipe += [rcp for tr in examples for rcp in list(tr) + ['']]

                return recipe

            dish_recipe = prepare_dish_recipe(
                self.LANGS[self.source_lang],
                len(self.the_dinner.keys())
            )
            if dish_recipe:
                self.dinner_recipe.append(dish_recipe)

            self.the_dinner[target] = dish

    def dinner(self):
        dishes_count = len(self.the_dinner.keys())
        print(f'There is {dishes_count}-dish dinner!', file=sys.stderr)
        for line in self.dinner_recipe:
            print(*line, sep='\n')


"""
Pass `-t` to the command that starts the program for local tests
"""
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')
if parser.parse_args().test:
    # Translator().translate(3, 4, 'hello')
    # Translator().translate(3, 0, 'hello')
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
