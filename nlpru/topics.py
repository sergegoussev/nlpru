# -*- coding: utf-8 -*-
"""
nlpru.topics
"""
from __future__ import print_function
from nlpru.clean import Cleaner
from nlpru.error import InputError
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
        self._tweet_dict = self._validate_input_(kwargs)
        
    def _validate_input_(self, kwargs):
        '''
        Validate the input used in the initiation of the object
        '''
        tweet_list_reqs = ['tweet_list','tweet_text_index','tweet_id_index']
        
        if 'tweet_dict' in kwargs:
            #validate that the dict is constructed correctly
            tweet_dict = kwargs['tweet_dict']
            if type(tweet_dict) is not dict:
                raise InputError("Imporperly constructed tweet_dict used")
            elif all('text' in tweet_dict[key].keys() for key in tweet_dict) == False:
                raise InputError("Improperly constructed tweet_dict, no tweet text found")
            else:
                return tweet_dict
        elif all(inp in kwargs for inp in tweet_list_reqs):
            #validate that the list errors are correct and if so, construct the dict
            tweet_list = kwargs['tweet_list']
            if type(tweet_list) is not list:
                raise InputError("Improper tweet_list inputted")
            else:
                try:
                    tweet_text_index = kwargs['tweet_text_index']
                    tweet_id_index = kwargs['tweet_id_index']
                    #figure our which indexes have been given and the ones that havent
                    list_of_avail_index = [i for i in range(1,len(tweet_list[0])+1) \
                                           if i not in [tweet_text_index,tweet_id_index]]
                    other_vars = [[each[i-1] for i in list_of_avail_index] \
                                  for each in tweet_list]
                    return {each[tweet_id_index]:{
                            'text':each[tweet_text_index],
                            'other':other_vars} for each in tweet_list
                            }
                except Exception as e:
                    raise InputError("Improper tweet_list inputted")
 
    #--------Methods-------------------------------------------------------------------------
    def Keyword_Match(self, topic_dict):
        for tweet in self._tweet_dict:
            clean_words = self.__clean_words__(self._tweet_dict[tweet]['text'])
            self._tweet_dict[tweet]['clean_words'] = clean_words
            topic = "none_detected"
            num_assigned = 0
            for each_topic in topic_dict:
                print(each_topic, tweet)
                if len(set(topic_dict[each_topic]).intersection(clean_words)) != 0:
                    topic = each_topic
                    num_assigned += 1
            if num_assigned == 1:
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
            '111':{'text':'вот почему б не указать'},
            '222':{'text':"наш Самарский расследование"},
            '333':{'text':"вот он не бот"},
            '444':{'text':'можно обратиться напрямую'},
            '555':{'text':"какое расследование"}
            }
    topic_dict = {
            "11111111":["почему", "наш"],
            "22222222":["расследование","какой"]
            }
#    print(hasattr(tweet_dict, 'text'))
    T = FindTopics(tweet_dict=tweet_dict)
    r = T.Keyword_Match(topic_dict)
#    print(r)
