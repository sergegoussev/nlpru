# -*- coding: utf-8 -*-
"""
nlpru.topics
"""
from nlpru import Cleaner
from nlpru import InputError

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
            elif 'text' not in tweet_dict:
                raise InputError("Imporperly constructed tweet_dict, no tweet text found")
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
                    other_vars = [[each[i-1] for i in list_of_avail_index] for each in tweet_list]
                    return {each[tweet_id_index]:{
                            'text':each[tweet_text_index],
                            'other':other_vars} for each in tweet_list
                            }
                except Exception as e:
                    raise InputError("Improper tweet_list inputted")
 
    #--------Methods-------------------------------------------------------------------------
    def Keyword_Match(self, topic_dict):
        final_list_of_tweets = []
        for tweet in self._tweet_dict:
            for topic in topic_dict:
                clean_words = __check_words_in_doc__(tweet[0])
                if len(set(keywords).intersection(clean_words)) != 0:
                    topic = "Protests"
                else:
                    topic = "others"
                final_list_of_tweets.append()
                
                

if __name__ == '__main__':
    pass