"""
Local translator with remote translating.
"""

import argparse

from exceptions import NothingToTranslateError
from online_translator import OnlineTranslator


def main():
    parser = argparse.ArgumentParser(
        exit_on_error=False,
        description='Local translator with remote translating.'
    )
    parser.add_argument('source_lang', type=str, nargs='?',
                        help='Number of source language.')
    parser.add_argument('target_lang', type=str, nargs='?',
                        help='Number of target language or "all" to '
                             'translate to '
                             'all available languages.')
    parser.add_argument('word', type=str, nargs='?',
                        help='The word to translate.')
    parser.add_argument('-t', '--test', action='store_true',
                        help='enable test mode with local tests')

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
        """Local testing."""
        OnlineTranslator().translate('english', 'all', 'love')
        OnlineTranslator().translate('spanish', 'english', 'derechos')
        exit('Enjoy the translations!')

    if each_of:
        if args_dict['source_lang'] == args_dict['target_lang']:
            exit(NothingToTranslateError(
                args_dict['source_lang'].capitalize(),
                args_dict['target_lang'].capitalize(),
            ))

        source_lang = args_dict['source_lang']
        target_lang = args_dict['target_lang']
        word = args_dict['word']

        # Engage 🚀
        translator = OnlineTranslator()
        translator.translate(source_lang, target_lang, word)


if __name__ == '__main__':
    main()
