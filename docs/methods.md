[Home](../README.md) | [examples](../examples/README.md)

# Methods walkthrough

The following walks through the methods availible

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