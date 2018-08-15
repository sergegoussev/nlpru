# -*- coding: utf-8 -*-
"""
nlpru.conversation
"""
from __future__ import print_function
from nlpru.error import ConversationError
from nlpru.models import validate_tweet_input

class Conversations:
    """
    ConversationTopicer changes the topic of tweets not categorized about a topic 
    to the topic by checking the conversation thread affects.  
    """
    def __init__(self, **kwargs):
        """
        @parameters:
        - retweet_list - list of retweets in the manner of 
            [('tweet id','retweeted tweet id'),...]
        - reply_list - list of all replies in the manner of 
            [('tweet id','replyng to tweet id'),...]
        - quote_list - list of all times a quote is made in the manner of
            [('tweet id','quoting tweet id'),...]
        """
        self._validate_input_(kwargs)
            
    def _validate_input_(self, kwargs):
        """
        Validate and convert the vars that were created
        """
        try:
            if 'retweet_list' in kwargs:
                self._retweets = {each[0]:each[1] for each in kwargs['retweet_list']}
            else:
                self._retweets = []
            if 'quote_list' in kwargs:
                self._quotes = {each[0]:each[1] for each in kwargs['quote_list']}
            else:
                self._quotes = []
            if 'reply_list' in kwargs:
                self._replies = {each[0]:each[1] for each in kwargs['reply_list']}
            else:
                self._replies = []
        except Exception as e:
            raise ConversationError("Improper input for Conversations:"+ str(e))           

    #----------------------main function---------------------------------------------
    def Recategorize_topics(self, 
                            topic_for_which_to_check, 
                            no_topic_label="none detected",
                            **kwargs):
        """
        Check and recategorize the tweets NOT about the topic but should be
        
        @parameters:
            - no_topic_label - what is the label of topics that have no label
                    associated with them. 
                default - 'none detected'
            - topic_for_which_to_check - what is the label you want to check for?
                for ex: topic_for_which_to_check = 'topic 1'
                
        @other parameters - tweets
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
                    

        @returns: dict of tweets and their topics 
        """
        self._topic_for_which_to_check = topic_for_which_to_check
        self._no_topic_label = no_topic_label
        self._tweet_dict = validate_tweet_input(kwargs)
        return self._recategorize_mast_()
        
    #----------------------supporting functions-----------------------------------------
    def _recategorize_mast_(self):
        """
        main function that recagorizes tweets based on the initial input of tweets
        """
        #create a copy of the original tweet dict to work with
#        tweet_dict = self._tweet_dict.copy()
        i = 1
        while True:
            n_changed = 0
            #iterate over all the tweets in the master input dict
            for tweet, value in self._tweet_dict.items():
                #only check and change the topic if the topic was NOT on the topic of interest
                if value['topic'] == self._no_topic_label:
                    result = self._recategorize_check_tweet_(tweet)
                    if result == "change":
                        self._tweet_dict[tweet]['topic'] = self._topic_for_which_to_check
                        n_changed += 1
            print("{i} iteration completed, recategorized this round: {n}".format(i=i,n=n_changed))
            i += 1
            #if no more tweets are being changed, exit the loop
            if n_changed == 0:
                break
        return self._tweet_dict
    
    def _recategorize_check_tweet_(self, twtid):
        """
        check the tweet that is inputted as about the applicable rules
        """
        #default 'result' of the check is None. If a match is made with any of the convo links, 
        #then 'result' is updated. 
        result = None
        #check replies -- if this tweet was a reply to the other tweet
        if twtid in self._replies and self._replies[twtid] in self._tweet_dict:
            #check if the topic of the replied to tweet was on the topic we are listening to
            if self._tweet_dict[self._replies[twtid]]['topic'] == self._topic_for_which_to_check:
                result = "change"
        #check quotes -- if this tweet quoted another tweet
        if twtid in self._quotes and self._quotes[twtid] in self._tweet_dict:
            #now check if the topic of the quoted tweet was on the topic of interest 
            if self._tweet_dict[self._quotes[twtid]]['topic'] == self._topic_for_which_to_check:
                result = "change"
        #check retweets -- if this tweet retweeted another tweet
        if twtid in self._retweets and self._retweets[twtid] in self._tweet_dict:
            #if the retweeted tweet was on the topic, then change the retweeting tweet topic
            if self._tweet_dict[self._retweets[twtid]]['topic'] == self._topic_for_which_to_check:
                result = "change"
        return result
    
    
if __name__ == '__main__':
    from nlpru import FindTopics
    tweet_dict = {
                '1':{'text':'вот почему б не указать'},
                '2':{'text':"наш Самарский расследование"},
                '3':{'text':"вот он не бот"},
                '4':{'text':'можно обратиться напрямую'},
                '5':{'text':"какое расследование"},
                '6':{'text':'обратиться ... напрямую'},
                }
    topic_dict = {
                "topic 1":["почему", "наш"],
                "topic 2":["расследование","какой"]
                }
    replies = [('6','1')]
    
    T = FindTopics(tweet_dict=tweet_dict)
    r = T.Keyword_Match(topic_dict)
    
    c = Conversations(reply_list=replies)
    t = c.Recategorize_topics(topic_for_which_to_check="topic 1", tweet_dict=tweet_dict)
    
    
    