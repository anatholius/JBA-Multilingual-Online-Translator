"""
Local translator with remote translating.
"""

import argparse
import sys

import requests
from bs4 import BeautifulSoup


# speed up download
# session = requests.Session()


class Translator:
    LANGS = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew',
             'japanese', 'dutch', 'polish', 'portuguese', 'romanian',
             'russian', 'turkish', ]
    ADDRESS = 'https://context.reverso.net/translation'

    source_lang: int = None
    target_lang: int = None
    translation_board: list = []
    translations_board = {}
    word: str
    translations: list
    examples: zip

    def __init__(self):
        """
        Welcome in Translator :)
        """
        print(*[
            'Hello, welcome to the translator. Translator supports:',
            *[f'{i + 1}. {L.capitalize()}' for i, L in enumerate(self.LANGS)]
        ], sep='\n')

    def direction(self, target_lang: str = None):
        """
        Prepare direction string for URL.
        """

        if target_lang is None:
            target_lang = self.target_lang
        return f'{self.LANGS[self.source_lang]}-{target_lang}'

    def translate(self, source: str, target: str, word: str):
        """
        Main translation action in class.
        """
        source = self.LANGS.index(source)
        if target in self.LANGS:
            target = self.LANGS.index(source)
        else:
            target = 0
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

        # print report
        self.report()

    def store_translation(self):
        """
        Save `self.translations_board` to file.
        """

        file_name = f'{self.word}.txt'

        with open(file_name, 'w') as file:
            lines = [f'{r}\n' for rcp in self.translation_board for r in rcp]
            file.writelines(lines)
            print(f'File "{file_name}" saved.', file=sys.stderr)

    def translate_online(self, target: str, word: str):
        """
        Request to `context.reverso` for translation and store retrieved
        translations in instance attribute.

        After that this attribute is used for file storage and console
        output, without repeating the same steps
        """

        target_lang = target.capitalize()
        url = f'{self.ADDRESS}/{self.direction(target)}/{word}'
        print(f'Request for {target_lang} translation to: {url}')

        r = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'text/html; charset=utf-8'
        })
        # print(f'{r.status_code} {r.reason}')
        print('url', url)
        if len(r.history):
            exit(
                f'\nCannot translate the word "{word}" from language '
                f'"{Translator.LANGS[source_lang - 1].capitalize()}" to '
                f'language '
                f'"{target_lang}"\n'
            )
        # print('r.history', r.history)
        # print('r.is_redirect', r.is_redirect)
        # print('session', session)
        # exit('stop request')

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

            # Complete lang translation board for all translations board
            lang_translation_board = {
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
                t = lang_translation_board['translations']
                print(t)
                translations = [t[0]] if translations_count > 1 else t
                recipe += translations

                recipe.extend(['', f'{target_language} Examples:'])

                e = lang_translation_board['examples']
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

            self.translations_board[target] = lang_translation_board

    def report(self):
        """
        Print report to console for tests purposes
        """

        translations_count = len(self.translations_board.keys())
        print(
            f'There is translations board with {translations_count} '
            f'languages!',
            file=sys.stderr
        )
        for line in self.translation_board:
            print(*line, sep='\n')


parser = argparse.ArgumentParser(
    exit_on_error=False,
    description='Local translator with remote translating.'
)
parser.add_argument('-t', '--test', action='store_true',
                    help='enable test mode with local tests')
parser.add_argument('source_lang', type=str, nargs='?',
                    help='Number of source language.')
parser.add_argument('target_lang', type=str,
                    nargs='?',
                    help='Number of target language or "all" to translate to '
                         'all available languages.')
parser.add_argument('word', type=str,
                    nargs='?',
                    help='The word to translate.')

args = parser.parse_args()
args_dict = args.__dict__


def get_index(value):
    return (
        (value and value in args_dict.values())
        and list(args_dict.keys())[list(args_dict.values()).index(value)]
        or None
    )


one_of = (
    get_index(args.source_lang)
    or get_index(args.source_lang)
    or get_index(args.word)
)
each_of = (
    get_index(args.source_lang)
    and get_index(args.source_lang)
    and get_index(args.word)
)

if parser.parse_args().test:
    # exit('Local tests:')
    # Translator().translate(3, 4, 'hello')
    # Translator().translate(3, 0, 'hello')
    # Translator().translate(12, 3, 'глаза')
    Translator().translate('english', 'all', 'love')
    exit('Enjoy the translations!')

if each_of:
    print('args_dict', args_dict)
    if args_dict['source_lang'] == args_dict['target_lang']:
        print('\nThere is nothing to translate from {} to {}!\n'.format(
            args_dict['source_lang'].capitalize(),
            args_dict['target_lang'].capitalize(),
        ), file=sys.stderr)
        exit()

    source_lang = args_dict['source_lang']
    target_lang = args_dict['target_lang']
    word = args_dict['word']

    # print(source_lang, target_lang, word)
    # exit('stop')
    Translator().translate(
        source_lang,
        target_lang,
        word,
    )
else:
    exit("""
usage: translator.py [-h] [-t] source_lang target_lang word
translator.py: error: the following arguments are required: {missing_args}
""".format(
        missing_args=', '.join([k for k, v in args_dict.items() if v is None])
    ))
