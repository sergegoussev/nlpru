# -*- coding: utf-8 -*-
"""
nlpru.models

contains all cleaners, and misc functions required by other functions within the library
"""
from nlpru.error import InputError

def validate_tweet_input(kwargs):
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


if __name__ == '__main__':
    pass