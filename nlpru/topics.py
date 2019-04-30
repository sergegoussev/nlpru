# -*- coding: utf-8 -*-
"""
nlpru.topics
"""
from __future__ import print_function
from nlpru.clean import Cleaner
from nlpru.models import Convert_to_tweet_dictionary
from nlpru.error import TopicModelError

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
        self._tweet_dict = Convert_to_tweet_dictionary(**kwargs)

    # --------Methods-------------------------------------------------------------------------
    def Keyword_Match(self, topic_dict):
        """
        Keyword_Match() is the main method to see if a tweet contains a set of 
        keywords required
        
        @parametrs:
            - topic_dict - a dictionary of keywords to search of the following 
            pattern: 
                
        topic_dict = {
                "topic 1": {'contains':["word1", "word2"],'not':['word3']},
                "topic 2": {'contains':["word4", "word5"]},
                "topic 3": ["word6","word7"]
        }
        
        - each topic must have a title ("topic 1") - this will be applied as a 
        category to the tweet
        - 'contains' represents those keywords to be checked
            - NOTE: 'contains' can be skipped and passed in just as a list of words
        - 'not' (optional) represents those keywords that should NOT be present 
        in the tweet to be categorized as part of "topic 1"
            - NOTE: This is optional, and the presence of the 'not' object is 
            not necessary
            
        @output:
            - the output is a dictionary of tweets with the applied topic categories
        """
        #validate construction of topic_dict
        topic_dict = self.__validate_topic_dict_construction__(topic_dict)
        #iterate through the topics inputted
        for tweet in self._tweet_dict:
            print("="*30,tweet)
            #clean each word in the tweet (tokenize, lemmatize, etc)
            clean_words = self.__clean_words__(self._tweet_dict[tweet]['text'])
            self._tweet_dict[tweet]['clean_words'] = clean_words
            topic = "none detected"
            num_assigned = 0
            #iterate through possible list of topics
            for each_topic in topic_dict:
                #if keywords match those that 'contains' and NOT those 'not', 
                #categorize the tweet by topic
                print("-"*10,each_topic,"-"*10)
                print(topic_dict[each_topic]['contains'])
                print(clean_words)
                print(len(set(topic_dict[each_topic]['contains']).intersection(clean_words)))
                print(len(set(topic_dict[each_topic]['not']).intersection(clean_words)))
                
                if len(set(topic_dict[each_topic]['contains']).intersection(clean_words)) != 0:
                    if len(set(topic_dict[each_topic]['not']).intersection(clean_words)) == 0:
                        topic = each_topic
                        num_assigned += 1
            if num_assigned <= 1:
                self._tweet_dict[tweet]['topic'] = topic
            if num_assigned == 2:
                self._tweet_dict[tweet]['topic'] = 'applies to 2 topics'
            if num_assigned > 2:
                self._tweet_dict[tweet]['topic'] = 'applies to more than 2 topics'
        return self._tweet_dict
    
    def __validate_topic_dict_construction__(self, topic_dict):
        """
        __validate_topic__() converts the inputted topic_dict with the allowed
        flexibilities, and converts it into the format required for Keyword_Match()
        """
        for each_topic in topic_dict:
            try:
                if 'contains' not in topic_dict[each_topic]:
                    if type(topic_dict[each_topic]) == list:
                        temp_list = topic_dict[each_topic]
                        topic_dict.pop(each_topic)
                        topic_dict[each_topic] = {'contains':temp_list}
                    else:
                        raise TopicModelError("improper topic dictionary construction, 'conains' missing")
#                print(topic_dict)
                if 'not' not in topic_dict[each_topic]:
                    topic_dict[each_topic]['not'] = []
            except Exception as e:
                raise TopicModelError("Error in validating topic_dict: {}".format(e))
        print(topic_dict)
        return topic_dict

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
        '1': {'text': 'вот почему б не указать'},
        '2': {'text': "наш Самарский расследование"},
        '3': {'text': "вот он наш не бот"},
        '4': {'text': 'можно обратиться напрямую'},
        '5': {'text': "какое расследование"}
    }
    topic_dict = {
        "topic 1": {'contains':["почему", "наш"],'not':['бот']},
        "topic 2": {'contains':["расследование", "какой"]},
        "topic 3": ['бот']
    }
    T = FindTopics(tweet_dict=tweet_dict)
    r = T.Keyword_Match(topic_dict)
#    print(r)
