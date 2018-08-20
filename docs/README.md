[Home](../README.md) | Documentation  | [Methods](methods.md) | [Examples](../examples/README.md)

# welcome to the *nlpru* documenation

As you probably read in the home page, **nlpru** is a library meant to simplify Natural Language Processing and analysis of Russian text. While it is built for *Twitter* and for Russian language text, it can be used for Ukrainian text as well, and certain *methods* can be used as well as they are not language specific.

# reason for using **nlpru** 

The library makes it easy to use several methods commonly used with *natural language processsing*, such as categorizing tweets by topic, preprocessing (or cleaning text), etc. While several other libraries exist that can do many of these things, I found that general ones such as [**preprocessor**](https://github.com/s/preprocessor) don't seem to work well with Russian text. Russian specific libraries, such as [**pymorphy2**](https://github.com/kmike/pymorphy2) (which **nlpru** uses behind the scenes) offer useful NLP morphological analysis but not preprocessing or facilitation of different types of analysis.

## Installation

The *nplru* library is not yet availible via *Pypi*, hence to install it, it has to be downloaded from this gitab repository. This means there are two ways to do it:

You can install this library via git from github directly: 

    >>> pip install git+https://github.com/sergegoussev/nlpru.git

Or you can download the repo zip, and then use pip in the folder:

    >>> pip install .

## Methods

In the current version, there are 4 main methods and one supporting method available.

Main methods:
* [Analyze document semantics and cosine similairty](methods.md#semantics)
* [Clean or preprocess text](methods.md#preprocessing)
* [Categorize topics of tweets](methods.md#topic-analysis)
* [Adding Conversation thread effects to Topic Analysis](methods.md#add-conversation-affects-to-topics) 

Supporting methods:
* **nlpru** uses a dictionary method to support the **Topic Analysis** and **Conversation thread** methods. If you want to manually use the dictionary conversion method, you can read [about how to use it here](methods.md#convert-to-tweet-dictionary)