# checkword
Simple module for check if the text contains blacklisted or whitelisted words

##Installation
```
pip install checkword
```

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