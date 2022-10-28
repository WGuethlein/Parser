class Token:
    __category = None
    __lineNumber = None
    __word = None

    def __init__(self, category, lineNumber, word):
        self.__category = category
        self.__lineNumber = lineNumber
        self.__word = word

    def category(self):
        return self.__category

    def lineNumber(self):
        return self.__lineNumber

    def word(self):
        return self.__word
