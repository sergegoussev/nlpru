# nlpru

**nlpru** is a simple library to help conduct Natural Language Processing analysis of Russian text. It is built with Russian language social media data in mind.

Some other libraries, such as [**preprocessor**](https://github.com/s/preprocessor) don't seem to work well with Russian text. Hence this library is a WIP attempt to bridge this gap.

~WIP~

# key methods

There are two main methods built in at this point: *Clean* or preprocessing and *Semantics* or NLP methods -- right now only Semantic Similarity.

```python
#import library
from nlpru import Clean

#initiate the Clean method
c = Clean()

#initiate the Semantics method
s = Semantics()
```
## Semantics module

This module has one object with (currently) one method - the calculation of *cosine similarity* between documents. The method underlying it is tf-idf.

```python

docs = [doc1, doc2]
print(s.Get_similarity(doc))
```

## Clean module

Two Clean methods exist, one to clean the document (i.e. the tweet), and another to check whether the word should be included in subsequent bag-of-words analysis (for instance Frequency Distribution)

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
