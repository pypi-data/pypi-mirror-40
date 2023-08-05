from .processor import Processor

__whitelist = Processor()
__blacklist = Processor()


def blacklisted(text, match_case=False, words=True):
    """
    Check if text contains blacklisted words
    :param text:
    :param match_case:
    :param words:
    :return:
    """
    return __blacklist.check_text(text, match_case=match_case, words=words)


def whitelisted(text, match_case=False, words=True):
    """
    Check if text contains whitelisted words
    :param text:
    :param match_case:
    :param words:
    :return:
    """
    return __whitelist.check_text(text, match_case=match_case, words=words)


def add_bad_words(words):
    """
    Add bad words to blacklist.
    :param words:
    """
    __blacklist.update_container(words)


def add_good_words(words):
    """
    Add good words to whitelist.
    :param words:
    """
    __whitelist.update_container(words)


def remove_bad_word(word):
    """
    Remove bad word from blacklist.
    :param word:
    """
    __blacklist.remove(word)


def remove_good_word(word):
    """
    Remove word from list. `list_type` must be one of blacklist and whitelist
    :param word:
    """
    __whitelist.remove(word)


def clear_blacklist():
    """
    Clears blacklist words
    """
    __blacklist.clear()


def clear_whitelist():
    """
    Clears whitelist words
    """
    __whitelist.clear()
