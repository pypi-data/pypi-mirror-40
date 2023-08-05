# checkword
Simple module for check if the text contains blacklisted or whitelisted words

# Installation
```
pip install checkword
```
---
## Usage
```python
import checkword

# add some bad words to blacklist
checkword.add_bad_words(['some', 'bad', 'words', 'like', 'sheet'])

# and good words
checkword.add_good_words(['Festival', 'Event', 'Holiday'])

print(checkword.blacklisted('My some text to check for bad words'))
# True

print(checkword.whitelisted('Another text to check for good words'))
# False
```
---
### Methods

**add_bad_words(words)**
> add word or words list/tuple to blacklist

**add_good_words(words)**
> add word or words list/tuple to whitelist

**blacklisted(text, match_case=False, words=True)**
> check if text contains any bad words\
**text**: text for checking\
**match_case**: use case sensitive word matching. 
if True `checkword.blacklisted('bAd')` will be False when `'bad'` is in blacklist \
**words**: match only complete words. if True `checkword.blacklisted('my bad string')=True` and `checkword.blacklisted('mybadstring')=False` while `'bad'` is in blacklist

**whitelisted(text, match_case=False, words=True)**
> check if text contains any whitelisted words\
**text**: text for checking\
**match_case**: use case sensitive word matching. 
if True `checkword.whitelisted('gOoD')` will be False when `'good'` is in blacklist \
**words**: match only complete words. if True `checkword.whitelisted('my good string')=True` and `checkword.whitelisted('mygoodstring')=False` while `'good'` is in blacklist

**remove_bad_word(word)**
> remove bad word from blacklist

**remove_good_word(word)**
> remove good word from whitelist

**clear_blacklist()**
> remove all bad words from blacklist

**clear_whitelist()**
> remove all good words from whitelist