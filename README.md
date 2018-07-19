# nlpru

**nlpru** is a simple library to support Natural Language Processing analysis of Russian text. It is built with Russian language social media data in mind.

Several other libraries I have tried, such as [**preprocessor**](https://github.com/s/preprocessor) don't seem to work well with Russian text. Others such as [**pymorphy2**](https://github.com/kmike/pymorphy2) (on which this library is partly based) offer useful NLP morphological analysis but not preprocessing.

**WIP** -- Some feature are not fully buit and tested at this time.

# installation

You can install this library via git from github directly: 

    >>> pip install git+https://github.com/sergegoussev/nlpru.git

# key methods

There are two main methods built in at this point: *Clean* or preprocessing and *Semantics* to deterimine cosine similarity.

To initiate either method, you first need to:

```python
#import library
from nlpru import Clean

#initiate the Clean method
c = Clean()

#initiate the Semantics method
s = Semantics()
```
## Semantics

This module has one object with (currently) one method - the calculation of *cosine similarity* between documents. The method underlying it is tf-idf.

```python

docs = [doc1, doc2]
print(s.Get_similarity(doc))
```

## Clean

Clean allows the preprocessing of text, with two methods availible: one to clean the document (i.e. the tweet or post), and another to check whether a word should be included in subsequent bag-of-words analysis -- to remove stop words, emojis, etc.

**Clean_document**
```python
raw = "Все говорят забудь его, забудь... а вот вы можете ..."
c.Clean_document(raw)
#"Все говорят забудь его забудь а вот вы можете"
```
Parameters with defaults:
* remove_RTs = True
* remove_hashtags = True
* remove_mentions = True
* remove_urls = True
* remove_emoji = True
* remove_swears = False
* remove_special_chars = True


**Check_word**
The result of Check_word is a dictionary 
```javascript
{'status':'ok OR empty','word':'clean word if applicable'}
```

Usage as follows:
```python
word = "твердил"
result = c.Check_word(word)

print(word, result)
#твердил {'status': 'ok', 'word': 'твердить'}

#a few other examples:
#Можно {'status': 'empty', 'word': ''}
#слабому {'status': 'ok', 'word': 'слабый'}
#имеет {'status': 'ok', 'word': 'иметь'}
```
Parameters with defaults:
* lemmatize = True 
* remove_proper_nouns = True
* allow_acronyms = False 
* exclude_english_words = True
