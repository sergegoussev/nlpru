# -*- coding: utf-8 -*-
"""
nlpru.clean
"""
from __future__ import print_function
import pymorphy2
import string
import re
import emoji
import nltk
import sys
#from nltk import word_tokenize
from nlpru import stop_words as tsw
from nltk.corpus import stopwords

# --------------------------
# create stopwords and lemmatization
stop = stopwords.words('russian')
exclude = list(string.punctuation)
morph = pymorphy2.MorphAnalyzer()
for each in tsw.sw:
    exclude.append(each)

swears = tsw.swear_words
# alphabet + number match - check only russian words and not english
ru_alphabet = list(tsw.ru_alphabet)
en_alphabet = list(tsw.en_alphabet)
en_alphabet.append('і')
numbers = list(tsw.numbers)
consonants = list(tsw.ru_consonants)

emojis = ''.join(each for each in emoji.UNICODE_EMOJI)

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
# --------------------------


class Cleaner:
    '''
    The Cleaner object works by cleaning a specified piece of text for
    natural language analysis
    '''

    def __init__(self, language='ru'):
        if language != 'ru':
            print('Unable to process other languages at this time')

    def Clean_document(self,
                       input_document,
                       remove_RTs=True,
                       remove_hashtags=True,
                       remove_mentions=True,
                       remove_urls=True,
                       remove_emoji=True,
                       remove_swears=False,
                       remove_special_chars=True):
        '''
        Clean_tweet - cleans the tweet, removing all mentions, urls,
        hashtags, and emojis

        input:
        - input_tweet - must be string
        output:
        - string that excludes emojis, mentions, urls, etc

        Options include:
         - remove_hashtags
         - remove_mentions
        '''
        doc = input_document
        # RTs
        if remove_RTs == True:
            doc = re.sub('RT (.*?) ', '', doc)
        if remove_hashtags == True:
            doc = re.sub('#(.+?) ', '', doc)  # hashtags - in the middle
            doc = re.sub('#(.+?)$', '', doc)  # hashtags - in the end
        if remove_mentions == True:
            doc = re.sub('@\w* ', '', doc)  # mentions - in the middle
            doc = re.sub('@\w*$', '', doc)  # mentions - in the emd
        if remove_urls == True:
            # urls in the middle of the tweet
            doc = re.sub('http(.+?) ', '', doc)
            doc = re.sub('http(.+?)$', '', doc)  # urls at the end of the tweet
            # urls in the middle of the tweet
            doc = re.sub('http(.+?)\n', '', doc)
        if remove_emoji == True:
            doc = re.sub(emojis, '', doc)  # emojis version
        if remove_swears == True:
            doc = re.sub('твою мать', '', doc, re.IGNORECASE)
            for swear in swears:
                doc = re.sub(swear, '', doc, re.IGNORECASE)
        if remove_special_chars == True:
            doc = re.sub(
                """[→©ђ°ѓ¡|\|=/\\▶►‼?~é̄̃`«»;џ�_●▪™“„#ї*&%¿$\-\”<>'|/?~`\+\：«»;_“„&^№€…)(—]""", '', doc)
        doc = re.sub('\n', '.', doc)  # remove white spaces, i.e. new lines
        # validate that spaces that should exist actually exist
        for character in [',', r'\.', r'\?', r'!', r':', r';']:
            doc = re.sub(' '+character, character, doc)
            doc = re.sub(character, character+' ', doc)
        doc = re.sub(' +', ' ', doc)  # remove extra spaces
        doc = doc.strip()
        return doc

    def Check_word(self,
                   word,
                   lemmatize=True,
                   remove_proper_nouns=True,
                   allow_acronyms=False,
                   exclude_english_words=True):
        '''
        Check_word - checks if the word is good to be included for
        natural language analysis. It takes the specified word, and
        returns the a result dictionary.

        Result dictionary:
        - dictionary['word'] = the word
        - dictionary['status'] = the status. Possible statuses:
          > 'ok' - means the word is returned
          > 'empty' - means word is ''

        Thngs that are checked, if:
         - length is more than 2
         - if the letters match the russian alphabet
         - if there are no english alphabet letters
         - if there are no numbers in the word
         - if there are consonants in the word (so as to remove non-consonant
        acronyms)
         - if lemmatize=True (default), the normal form of the word is returned
         - if remove_proper_nouns=True (default), proper nouns (plural/singlular),
        usually place names or indivdual names, are removed
        '''
        result = {}
        if (word.lower() not in stop) and \
           (word.lower() not in exclude) and \
           len(set(word.lower()).intersection(set(ru_alphabet))) > 0 and \
           len(set(word.lower()).intersection(set(numbers))) == 0 and \
           len(word) > 2:
            result['word'] = word.lower()
            result['status'] = 'ok'
            if allow_acronyms == False and \
               len(set(word.lower()).intersection(set(consonants))) == 0:
                result['word'] = ''
                result['status'] = 'empty'
            if exclude_english_words == True and \
               len(set(word.lower()).intersection(set(en_alphabet))) > 0:
                result['word'] = ''
                result['status'] = 'empty'
            if lemmatize == True:
                word = morph.normal_forms(result['word'])[0]
                result['word'] = word
                if len(word) > 0:
                    result['status'] = 'ok'
                else:
                    result['status'] = 'empty'
            if remove_proper_nouns == True:
                if len(nltk.pos_tag([result['word']])[0]) > 0:
                    if nltk.pos_tag([result['word']])[0][1] == 'NNP' or \
                       nltk.pos_tag([result['word']])[0][1] == 'NNPS':
                        result['word'] = ''
                        result['status'] = 'empty'
            if (result['word'] in stop) and \
               (result['word'] in exclude):
                result['word'] = ''
                result['status'] = 'empty'

        else:
            result['word'] = ''
            result['status'] = 'empty'
        return result


if __name__ == '__main__':
    C = Cleaner()
    tweet = """п***ц какое расследование,почему б не указать,что наш Самарский ио @D_Azaroff ,вот он не бот,можно обратиться напрямую,не откажет \xF0\x9F\x98\x81
    """
    tweet2 = "п***ц какое расследование,почему"
    print(C.Clean_document(tweet, remove_swears=True, remove_mentions=False))
