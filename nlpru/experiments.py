# -*- coding: utf-8 -*-
"""
experiments
"""
from pysql import DB
from nlpru import Cleaner

import pymorphy2
from nltk import word_tokenize

db = DB('kremlin_protests_dw')

C = Cleaner('ru')

morph = pymorphy2.MorphAnalyzer()

def getdata():
    q = """
    SELECT 
    	twtid,
    	twttext 
    FROM kremlin_protests_dw.samp_twts_dimon_mar26_rest
    	WHERE author_username = 'navalny';
    """
    r = db.query(q)
    return r

def clean_data():
    C = Cleaner()
    tweets = []
    for tweet in r:
        t = ""
        t = C.Clean_tweet(tweet)
        for word in t.split():
            result = C.Check_word(remove_proper_nouns=False)
            if r['status'] is not 'empty':
                t += ' '+ result['word']
        tweets.append(t)
    return tweets

def main():
    clnts = []
    tweets_raw = getdata()
    for tweet in tweets_raw:
        clnts.append((tweet[0],
                      C.Clean_tweet(tweet[1])))
    return clnts
    
