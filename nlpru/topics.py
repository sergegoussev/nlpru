# -*- coding: utf-8 -*-
"""
nlpru.topics
"""
from nlpru import Cleaner

class Topics:
    """
    To detect topics, choose a choise of method, and pass in the required inputs
    """
    def __init__(self):
        C = Cleaner()
    
    def Keywords(self, tweet_list, topic_dict):
        final_list_of_tweets = []
        for tweet in tweet_list:
            for topic in topic_dict:
                clean_words = __check_words_in_doc__(tweet[0])
                if len(set(keywords).intersection(clean_words)) != 0:
                    topic = "Protests"
                else:
                    topic = "others"
                final_list_of_tweets.append((tweet[3], topic, tweet[0], clean_words, tweet[1], tweet[2]))