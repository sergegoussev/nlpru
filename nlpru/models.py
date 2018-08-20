# -*- coding: utf-8 -*-
"""
nlpru.models

contains all cleaners, and misc functions required by other functions within the library
"""
from nlpru.error import InputError

def Convert_to_tweet_dictionary(**kwargs):
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
                vars_to_get = [i for i in range(1,len(tweet_list[0])) \
                                   if i not in [tweet_text_index,tweet_id_index]]
                d = {}
                for tweet in tweet_list:
                    
                    other_vars = [tweet[i] for i in vars_to_get]
                    d[tweet[tweet_id_index]] = {
                            'text':tweet[tweet_text_index],
                            'other':other_vars}
                return d
            except Exception as e:
                raise InputError("Improper tweet_list inputted")
    else:
        raise InputError("Improper tweet input, please either input tweet list or tweet dictionary")


if __name__ == '__main__':
    from pysqlc import DB
    db = DB('kremlin_tweets_db')
    q = """
    SELECT 
        tmast.twtid,
        tmast.twttext AS twttext,
        tmast.userid
    FROM samp_twts_all_rus_twts_str tsamp 
        INNER JOIN twt_Master tmast 
        ON tsamp.twtid=tmast.twtid
        
    WHERE tmast.twt_lang='ru'  
    AND tmast.twt_createdat >= '{start}'
    AND tmast.twt_createdat < '{end}'
    """.format(start='2017-03-26', end='2017-03-27')
    data = list(db.query(q))
    d = Convert_to_tweet_dictionary(tweet_list=data, tweet_text_index=1, tweet_id_index=0)
    