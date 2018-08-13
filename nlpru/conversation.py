# -*- coding: utf-8 -*-
"""
nlpru.conversation
"""
from __future__ import print_function
from nlpru.error import ConversationError


class Conversations:
    """
    ConversationTopicer changes the topic of tweets not categorized about a topic to the topic by 
    checking the conversation thread affects.  
    """
    def __init__(self, 
                 retweet_list,
                 reply_list, 
                 quote_list):
        """
        @parameters:
        - retweet_list - list of retweets in the manner of 
            [('tweet id','retweeted tweet id'),...]
        - reply_list - list of all replies in the manner of 
            [('tweet id','replyng to tweet id'),...]
        - quote_list - list of all times a quote is made in the manner of
            [('tweet id','quoting tweet id'),...]
        """
        try:
            self._replies = {each[0]:each[1] for each in reply_list}
            self._quotes = {each[0]:each[1] for each in quote_list}
            self._retweets = {each[0]:each[1] for each in retweet_list}
        except Exception as e:
            raise ConversationError("Improper input for Conversations:"+ str(e))

    #----------------------main function---------------------------------------------
    def Recategorize_topics(self, tweet_list, change_topic_label, no_topic_label="NA"):
        """
        Check and recategorize the tweets NOT about the topic but should be
        
        @parameter:
            - tweet_list - list of tweets with tuples, such as
                    [('twtid','topic',...),...]
                NOTE the first must be the tweet id, 
                    the second the topic label, 
                    further inputs are ignored and returned as is
            - no_topic_label - what is the label of topics that have no label
                    associated with them. 
                default - 'NA'
        @returns: dict of tweets and their topics 
        """
        self._change_topic_label = change_topic_label
        #first, just run the regular categorization and categorize based on keyword matches
        if len(tweet_list[0]) > 2:
            self._initial_tweet_dict = {
                    each[0]:{
                            'topic':each[1],
                            'other_params':[each[2:]]
                            } for each in tweet_list
                    }
        else:
            self.initial_tweet_dict = {each[0]:{'topic':each[1]} for each in tweet_list}
        self._no_topic_label = no_topic_label
        return self._recategorize_mast_()
        
    #----------------------supporting functions---------------------------------------------------
    def _recategorize_mast_(self):
        """
        main function that recagorizes tweets based on the initial input of tweets
        """
        #create a copy of the original tweet dict to work with
        tweet_dict = self._initial_tweet_dict.copy()
        i = 1
        while True:
            n_changed = 0
            #iterate over all the tweets in the master input dict
            for tweet, value in self._initial_tweet_dict:
                #only check and change the topic if the topic was NOT on the topic of interest
                if value['topic'] == self._no_topic_label:
                    result = self._recategorize_check_tweet_(tweet)
                    if result == "change":
                        tweet_dict[tweet]['topic'] == self._change_topic_label
                        n_changed += 1
            print("{i} iteration completed, recategorized this round: {n}".format(i=i,n=n_changed))
            i += 1
            #if no more tweets are being changed, exit the loop
            if n_changed == 0:
                break
        return tweet_dict
    
    def _recategorize_check_tweet_(self, twtid):
        """
        check the tweet that is inputted as about the applicable rules
        """
        #default 'result' of the check is None. If a match is made with any of the convo links, 
        #then 'result' is updated. 
        result = None
        #check replies -- if this tweet was a reply to the other tweet
        if twtid in self.replies and self.replies[twtid] in self.initial_tweet_dict:
            #check if the topic of the replied to tweet was on the topic we are listening to
            if self.initial_tweet_dict[self.replies[twtid]]['topic'] == self.change_topic_label:
                result = "change"
        #check quotes -- if this tweet quoted another tweet
        if twtid in self.quotes and self.quotes[twtid] in self.initial_tweet_dict:
            #now check if the topic of the quoted tweet was on the topic of interest 
            if self.initial_tweet_dict[self.quotes[twtid]]['topic'] == self.change_topic_label:
                result = "change"
        #check retweets -- if this tweet retweeted another tweet
        if twtid in self.retweets and self.retweets[twtid] in self.initial_tweet_dict:
            #if the retweeted tweet was on the topic, then change the retweeting tweet topic
            if self.initial_tweet_dict[self.retweets[twtid]]['topic'] == self.change_topic_label:
                result = "change"
        return result
    
    
    
if __name__ == '__main__':
    pass