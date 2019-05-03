nlpru homepage
==============

**nlpru** is a library meant to simplify Natural Language Processing and analysis of Russian text. It is built with Russian language social media data in mind, specifically *twitter*.

installation
------------

You can install this library via git from github directly: 

    >>> pip install git+https://github.com/sergegoussev/nlpru.git

quickstart
----------

Once installed, you can call each method you require by importing it from nlpru. For example, let's say you have some tweets to preprocess:

.. code-block:: python
    #import method
    from nlpru import Clean

    #initiate the method
    c = Clean()

    tweet = """п***ц какое расследование,почему б не указать,что наш Самарский ио @D_Azaroff
    ,вот он не бот,можно обратиться напрямую,не откажет"""

    #use the method and save its output
    clean_tweet = c.Clean_document(tweet, remove_swears=True)

If we print `clean_tweet`, it will return: 
`"какое расследование, почему б не указать, что наш Самарский ио @DAzaroff, вот он не бот, можно обратиться напрямую, не откажет"`

The library also offers some useful and simple methods, such as [categorizing topics and taking conversation threads into account](examples/Topic_and_conversation_thread_categorization_simple.ipynb)

documentation and examples
==========================

A full overview of the availible methods and examples is availible:
* `Documentation <https://sergegoussev.github.io/nlpru-docs/>`_
* [examples and walkthroughs](examples/README.md)