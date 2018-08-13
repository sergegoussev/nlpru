Home | [Documentation](docs/README.md) | [Examples](examples/README.md)

# nlpru

**nlpru** is a library meant to simplify Natural Language Processing and analysis of Russian text. It is built with Russian language social media data in mind, specifically *twitter*.

The library makes it easy to use several methods commonly used with *natural language processsing*, such as categorizing tweets by topic, preprocessing (or cleaning text), etc. While several other libraries exist that can do many of these things, I found that general ones such as [**preprocessor**](https://github.com/s/preprocessor) don't seem to work well with Russian text. Russian specific libraries, such as [**pymorphy2**](https://github.com/kmike/pymorphy2) (which **nlpru** uses behind the scenes) offer useful NLP morphological analysis but not preprocessing or facilitation of different types of analysis.

Designed for Python 3.5

*Author*: @sergegoussev

**WIP** -- some feature are not fully buit and tested at this time.

# installation

You can install this library via git from github directly: 

    >>> pip install git+https://github.com/sergegoussev/nlpru.git

Or you can download the repo zip, and then use pip in the folder:

    >>> pip install .

# quickstart

Once installed, you can call each method you require by importing it from nlpru. For example, let's say you have some tweets to process:

```python
#import library
from nlpru import Clean

#initiate the Clean method
c = Clean()

tweet = "п***ц какое расследование,почему б не указать,что наш Самарский ио @D_Azaroff ,вот он не бот,можно обратиться напрямую,не откажет )))"

print(c.Clean_document(tweet, remove_swears=True))
```

This will return 
`"какое расследование, почему б не указать, что наш Самарский ио @DAzaroff, вот он не бот, можно обратиться напрямую, не откажет"`

# documentation and examples

To have a fuller explanation of the availible methods, check out:
* [the documentation](docs/README.md)
* [examples and walkthroughs](examples/README.md)