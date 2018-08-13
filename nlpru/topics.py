# -*- coding: utf-8 -*-
"""
nlpru.topics
"""


class Detect_topics:
    
    
    def __init__(self):
        
        pass
        
    final_list_of_tweets = []
    for tweet in raw:
        clean_words = __check_words_in_doc__(tweet[0])
        if len(set(keywords).intersection(clean_words)) != 0:
            topic = "Protests"
        else:
            topic = "others"
        final_list_of_tweets.append((tweet[3], topic, tweet[0], clean_words, tweet[1], tweet[2]))