# nlpru

**nlpru** is a simple library to support Natural Language Processing analysis of Russian text. It is built with Russian language social media data in mind.

Several other libraries I have tried, such as [**preprocessor**](https://github.com/s/preprocessor) don't seem to work well with Russian text. Others such as [**pymorphy2**](https://github.com/kmike/pymorphy2) (on which this library is partly based) offer useful NLP morphological analysis but not preprocessing.

Designed for Python 3.5

**WIP** -- some feature are not fully buit and tested at this time.

# installation

You can install this library via git from github directly: 

    >>> pip install git+https://github.com/sergegoussev/nlpru.git

# quickstart

There are two main methods built in at this point: *Clean* or preprocessing and *Semantics* to deterimine cosine similarity.

To initiate either method, you first need to:

```python
#import library
from nlpru import Clean

#initiate the Clean method
c = Clean()

#initiate the Semantics method
s = Semantics()
```

# documentation and examples

To have a fuller explanation of the availible methods, check out:
* [the documentation](docs/README.md)
* [examples and walkthroughs](examples/README.md)