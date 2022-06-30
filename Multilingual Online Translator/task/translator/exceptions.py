class InternetConnectionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args

    def __str__(self) -> str:
        return "Something wrong with your internet connection"


class UnsupportedLanguageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args

    def __str__(self) -> str:
        return "Sorry, the program doesn't support %s" % self.args[0]


class UnsupportedTranslationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args

    def __str__(self) -> str:
        return "Sorry, unable to find %s" % self.args[0]


class NothingToTranslateError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args

    def __str__(self) -> str:
        return 'There is nothing to translate from {} to {}!'.format(
            self.args[0],
            self.args[1]
        )
