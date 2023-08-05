import re


class Processor:
    def __init__(self):
        self.container = set()

    def __word_check(self, text, match_case=False, words=True):
        reg = r'{}'
        if not match_case:
            text = text.lower()
        if words:
            reg = r'\b{}\b'
        for rule in self.container:
            if not match_case:
                rule = rule.lower()
            result = re.search(reg.format(rule), text)
            if result:
                return True
        return False

    def __add_words(self, words):
        if not isinstance(words, (list, tuple)):
            words = [words, ]
        self.container.update(words)

    def __remove_word(self, word):
        self.container.remove(word)

    def check_text(self, text, match_case, words):
        return self.__word_check(text=text, match_case=match_case, words=words)

    def update_container(self, obj):
        self.__add_words(obj)

    def remove(self, word):
        self.__remove_word(word)

    def clear(self):
        self.container.clear()
