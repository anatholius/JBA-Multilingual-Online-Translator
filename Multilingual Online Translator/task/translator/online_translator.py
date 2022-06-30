import sys

import requests
from bs4 import BeautifulSoup

# speed up download
session = requests.Session()


class OnlineTranslator:
    """
    Multilingual Online Translator class - JetBrains Academy project.
    """
    LANGS = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew',
             'japanese', 'dutch', 'polish', 'portuguese', 'romanian',
             'russian', 'turkish']
    ADDRESS = 'https://context.reverso.net/translation'

    source_lang: int = None
    target_lang: int = None
    reports: list = []
    translations: dict = {}
    word: str

    def __init__(self):
        """
        Welcome to Translator.
        """
        print(*[
            'Hello, welcome to the translator. Translator supports:',
            *[f'{i + 1}. {L.capitalize()}' for i, L in enumerate(self.LANGS)]
        ], sep='\n')

    def direction(self, target_language: str = None):
        """Prepare translation direction string for URL."""

        return '{source_lang}-{target_lang}'.format(
            source_lang=self.LANGS[self.source_lang],
            target_lang=target_language or self.target_lang
        )

    def translate(self, source: str, target: str, word: str):
        """Main translation action in class."""

        source = self.LANGS.index(source)
        if target in self.LANGS:
            target = self.LANGS.index(target)
        else:
            target = 0
        self.source_lang = source
        self.target_lang = target
        self.word = word

        if self.target_lang == 0:
            for t_lang_id, t_lang in enumerate(self.LANGS):
                if t_lang_id == self.source_lang:
                    continue
                self.translate_online(t_lang, word)
        else:
            target_language = self.LANGS[self.target_lang]
            self.translate_online(target_language, word)

        # store translations to file
        self.store_translations()

        # print report
        self.report()

    def store_translations(self):
        """Save `self.translations` to file."""

        file_name = f'./{self.word}.txt'

        with open(file_name, 'w') as file:
            lines = [f'{r}\n' for rcp in self.reports for r in rcp]
            file.writelines(lines)
            print(f'File "{file_name}" saved.', file=sys.stderr)

    def translate_online(self, target: str, word_to_translate: str):
        """
        Request to `context.reverso` for translation and store retrieved
        translations in instance attribute.

        After that this attribute is used for file storage and console
        output, without repeating the same steps
        """

        target_lang_name = target.capitalize()
        url = f'{self.ADDRESS}/{self.direction(target)}/{word_to_translate}'
        print(f'Request for {target_lang_name} translation to: {url}')

        r = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if len(r.history):
            print(
                'Redirection when translating online!\nCannot translate the '
                f'word "{word_to_translate}" from language '
                f'"{source_lang.capitalize()}" to language '
                f'"{target_lang_name}"\n',
                file=sys.stderr
            )
        elif r.ok:
            print(f'{r.status_code} {r.reason}')  # request status
            soup = BeautifulSoup(r.content, 'html.parser')

            # parse translations
            translations = [
                t.text for i, t in
                enumerate(soup.find_all('span', {'class': 'display-term'}))
            ]

            # parse examples
            source_soup = soup.find_all('div', {'class': 'src'})
            target_soup = soup.find_all('div', {'class': 'trg'})
            examples = [(a, b) for a, b in zip(
                [e.text.strip() for e in source_soup if e.text.strip()],
                [e.text.strip() for e in target_soup if e.text.strip()]
            )]

            if target != self.LANGS[self.source_lang]:
                # Complete translations board for all languages
                self.translations[target] = {
                    'translations': translations,
                    'examples': examples,
                }

                # Complete report board with prepared report
                self.reports.append([
                    f'{target.capitalize()} Translations:',
                    *self.translations[target]['translations'],
                    '',

                    f'{target.capitalize()} Examples:',
                    *[line
                      for example in self.translations[target]['examples']
                      for line in [*example, '']],
                    ''
                ])

    def report(self):
        """Print report to console."""

        translations_count = len(self.translations.keys())
        print(
            f'\nThere is translations board with {translations_count} '
            f'languages!\n',
            file=sys.stderr
        )
        for line in self.reports:
            print(*line, sep='\n')


if __name__ == '__main__':
    OnlineTranslator()
