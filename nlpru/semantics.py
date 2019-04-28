# -*- coding: utf-8 -*-
"""
nlpru.semantics
"""
from __future__ import print_function
import pymorphy2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nlpru import Cleaner

morph = pymorphy2.MorphAnalyzer()


class Semantics:
    '''
    The Semantics objects has a few attributes:
        - Get_similarity(
            - doc_list: list of documents for which to get semantic similarity
            - use_normal_form=False: lemmatization of all words present in document
            - stopwords=None: if you want to use a specific set of stop words
            - clean: clean the document to extract social media type content
                that will negatively impact analysis, such as hashtags, mentions
                urls, emoji, etc.
                attribute_types (specify what you want):
                    - None - do not clean document
                    - 'All' - remove everything (full list below)
                    - ['RT',
                       'hashtags',
                       'mentions',
                       'urls',
                       'emoji',
                       'swears',
                       'special_chars'] - if you want to remove specific things, 
                    specify any from the above as strings in a list, such as 
                    ['RT','mentions'] and only the specified ones will be cleaned
    '''

    def __init__(self, clean=None):
        self.C = Cleaner()
        if clean == None:
            self.clean = None
        elif clean == 'All':
            self.clean = ['RT',
                          'hashtags',
                          'mentions',
                          'urls',
                          'emoji',
                          'swears',
                          'special_chars']
        else:
            self.clean = clean

    def __lemmanization__(self,
                          input_document):
        """
        convert every word in a document into normal form
        """
        clean_document = ""
        for word in word_tokenize(input_document):
            w = morph.normal_forms(word)[0]
            clean_document += w + " "
        return clean_document

    def __normalize_docs__(self,
                           input_docs):
        '''
        convert all words in document to normal form
        '''
#        print('--------lemmatizing docs-----------')
        normalized_docs = []
        for doc in input_docs:
            #            print("-"*50)
            #            print("~~~~~~~~~~~~~original:~~~~~~~~~~~~~\n{}".format(doc))
            cln = self.__lemmanization__(doc)
            normalized_docs.append(cln)
#            print("~~~~~~~~~~~~~cleaned:~~~~~~~~~~~~~\n{}".format(cln))
        return normalized_docs

    def __clean_doc__(self, input_document):
        # specify the parameters to be passed in
        remove_RTs = False
        remove_hashtags = False
        remove_mentions = False
        remove_urls = False
        remove_emoji = False
        remove_swears = False
        remove_special_chars = False
        if self.clean is not None:
            if 'RT' in self.clean:
                remove_RTs = True
            if 'hashtags' in self.clean:
                remove_hashtags = True
            if 'mentions' in self.clean:
                remove_mentions = True
            if 'urls' in self.clean:
                remove_urls = True
            if 'emoji' in self.clean:
                remove_emoji = True
            if 'swears' in self.clean:
                remove_swears = True
            if 'special_chars' in self.clean:
                remove_special_chars = True
            # call the clean function
        x = self.C.Clean_document(input_document=input_document,
                                  remove_RTs=remove_RTs,
                                  remove_hashtags=remove_hashtags,
                                  remove_mentions=remove_mentions,
                                  remove_urls=remove_urls,
                                  remove_emoji=remove_emoji,
                                  remove_swears=remove_swears,
                                  remove_special_chars=remove_special_chars)
        return x

    def __clean_docs__(self, docs_list):
        #        print('------------cleaning docs-------------')
        cleaned_docs = []
        for doc in docs_list:
            #            print("-"*50)
            #            print("~~~~~~~~~~~~~original:~~~~~~~~~~~~~\n{}".format(doc))
            cln = self.__clean_doc__(doc)
            cleaned_docs.append(cln)
#            print("~~~~~~~~~~~~~cleaned:~~~~~~~~~~~~~\n{}".format(cln))
        return cleaned_docs

    def Get_similarity(self,
                       docs_list,
                       use_normal_form=False,
                       clean_documents=True,
                       stop_words=None,
                       similarity_to='first',
                       use_ngrams=True):
        """
        Get cosine similarity of documents. Uses sklearn's library and the 
        tf-idf approach (TfidfVectorizer()) to calcluate result

        (unique) params:
            - stop_words: list (or set) of stop words to use
            - similarity_to: 'first' or 'all' expected

        returns: 
            depending on 'similarity_to' param, either similarity row 
            vector of the first document to all others docs is returned, or
            (if 'All' is specified) matrix of of all docs against all others
        """
        if clean_documents == True:
            docs_list = self.__clean_docs__(docs_list)
        if use_normal_form == True:
            docs_list = self.__normalize_docs__(docs_list)
        if use_ngrams == True:
            tfidf_vectorizer = TfidfVectorizer(
                stop_words=stop_words, ngram_range=(2, 3))
        else:
            tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
        tfidf_matrix = tfidf_vectorizer.fit_transform(docs_list)
        cosine_similarity_matrix = cosine_similarity(
            tfidf_matrix[0:1], tfidf_matrix)
        return cosine_similarity_matrix


if __name__ == '__main__':
    S = Semantics(clean='All')
    docs = []
    docs.append(data[0][1])
    docs.append(data[0][3])
    print(S.Get_similarity(docs,
                           stop_words=stopWords))
