[Home](../README.md) |  [Documentation](README.md) | Methods | [Examples](../examples/README.md)

# Methods walkthrough

The following walks through the methods availible

## Semantics

If you want to determine *cosine similarity* between documents, you can use this method. You can use this for two tweets, two sets of tweets concatenated into 2 strings, or really any 2 string objects. The method underlying it is tf-idf.

```python
from nlpru import Similarity
s = Similiarity()

docs = [doc1, doc2]
print(s.Get_similarity(doc))
```

## Preprocessing

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

```python
from nltk.tokenize import word_tokenize 
raw = "Все говорят забудь его, забудь... а вот вы можете ..."

for word in word_tokenize(raw):
    c.Check_word(word)
```

Check_word returns a dictionary with a logical test: 
```javascript
{'status':'ok OR empty','word':'clean word if applicable or NA'}
```

For example:
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

## Topic Analysis

To assign tweets topics, you can specify the keywords you want to categorize a topic to, and *nlpru* will take care of the tagging for you. 

@input parameters:
* list_of_tweets -- input the tweets as a list. As for subsequent analysis you likely will want to get back the `tweet id`, a list of tuples, containg tweets and other variables is acceptable. 
    * in this case, specify the *tweet_location_in_tuple* parameter;
* tweet_location_in_tuple -- specify the integer location of the tweet within the each tuple -- for ex:
    * `list_of_tweets = [('twtid','twt_text),...], tweet_location_in_tuple=1`
    * **default**: `None`
* dictionary_of_topics -- specify your topics as dictionary keys and the keywords that apply to this topic as list in the value. For ex:
    * `topic_dict = {'protests':['navalny','putin'],'assasination':['voronenkov']}`

For example: 

```python
from nlpru import FindTopics

tweet_dict = {
            '1':{'text':'вот почему б не указать'},
            '2':{'text':"наш Самарский расследование"},
            '3':{'text':"вот он не бот"},
            '4':{'text':'можно обратиться напрямую'},
            '5':{'text':"какое расследование"}
            }
topic_dict = {
            "topic 1":["почему", "наш"],
            "topic 2":["расследование","какой"]
            }

#first call the overall method and give it the tweets as input
T = FindTopics(tweet_dict=tweet_dict) 
            
#now categorize the tweets by the keyword topic assigned
r = T.Keyword_Match(topic_dict)
```
    
**NOTE**: *nlpru* assumes that you will not try to categorize topics of identical tweets -- and finds the `twtid` in the list_of_tweets (if you specify a `dataframe` input for instance)

## Add conversation affects to topics

As tweets are not isolated in spacce but are usually part of a conversation thread, often with other tweets in a thread not using the listened to keywords, you can use this method to include conversation thread affects and categorize all *downstream* tweets as also on the parent tweet topic. 

For example, first find topics using the `FindTopics` method, then use the output dict to:

```python
from nlpru import Conversations

replies = [('6','1')]
    
c = Conversations(reply_list=replies)
t = c.Recategorize_topics(topic_for_which_to_check="topic 1", tweet_dict=tweet_dict)
```
    
For a full walkthrouh of the reasons why conversation thread affects need to be checked, see  [jupyter notebook walkthrough](../examples/Categorizing_by_topic_using_conversation_threads.ipynb).

## Convert to tweet dictionary

**nlpru** uses a dictionary method to process tweets -- both to categorize the topics and to assess conversation thread affects. For this it uses a dictionary structure:

```
tweet_dict = {
            '1':{'text':'вот почему б не указать'},
            '2':{'text':"наш Самарский расследование"},
            '3':{'text':"вот он не бот"},
            '4':{'text':'можно обратиться напрямую'},
            '5':{'text':"какое расследование"}
            }
```

While the method is built into others, if you want to call it separately, you can also do that:

```python
from nlpru import Convert_to_tweet_dictionary

tweet_dict = Convert_to_tweet_dictionary(
    tweet_list=[], 
    tweet_text_index=1,
    tweet_id_index=0)
```

This method can also validate that your `tweet_dict` is constructed correctly.