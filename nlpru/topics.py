# -*- coding: utf-8 -*-
"""
nlpru.topics
"""
from __future__ import print_function
from nlpru.clean import Cleaner
from nlpru.models import validate_tweet_input

from nltk.tokenize import word_tokenize

class FindTopics:
    """
    To detect topics, choose a choise of method, and pass in the required inputs
    """
    def __init__(self, **kwargs):
        """
        @parameters: 
            If you are inputting a list of tuples:
            - tweet_list -- specify list of tweets to categorize
            - tweet_text_index -- specify the index of the tweet text in the tuple;
                i.e. 0 for 1st, etc...
            - tweet_id_index -- specify the index of the tweet id (or unique tweet) 
                identifier.
            
            If you are inputting a dictionary of tweets, then the parameter should be:
            - tweet_dict - dictionary of tweets by twtid as the key
                - NOTE: the following dict is expected:
                    {'twtid':{'text':'bla bla bla ... ',...},....}
        """
        self._Cln = Cleaner()
        self._tweet_dict = validate_tweet_input(kwargs)
 
    #--------Methods-------------------------------------------------------------------------
    def Keyword_Match(self, topic_dict):
        for tweet in self._tweet_dict:
            clean_words = self.__clean_words__(self._tweet_dict[tweet]['text'])
            self._tweet_dict[tweet]['clean_words'] = clean_words
            topic = "none_detected"
            num_assigned = 0
            for each_topic in topic_dict:
#                print(each_topic, tweet)
                if len(set(topic_dict[each_topic]).intersection(clean_words)) != 0:
                    topic = each_topic
                    num_assigned += 1
            if num_assigned <= 1:
                self._tweet_dict[tweet]['topic'] = topic
            if num_assigned == 2:
                self._tweet_dict[tweet]['topic'] = 'applies to 2 topics'
            if num_assigned > 2:
                self._tweet_dict[tweet]['topic'] = 'applies to more than 2 topics'
        return self._tweet_dict

    def __clean_words__(self, document):
        """
        isolate the checking of words from a document into a separate function
        (for easier use later)
        """
        words = []
        for word in word_tokenize(document):
            result = self._Cln.Check_word(word, remove_proper_nouns=False)
            if result['status'] == 'ok':
                words.append(result['word'])
        return words
                

if __name__ == '__main__':
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
    T = FindTopics(tweet_dict=tweet_dict)
    r = T.Keyword_Match(topic_dict)
#    print(r)
    
