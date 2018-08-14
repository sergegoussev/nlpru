# -*- coding: utf-8 -*-
"""
nlpru.error
"""

class nlpruError(Exception):
    """
    The main exception handler for nlpru
    """
    def __init__(self, reason):
        Exception.__init__(self, reason)

class ConversationError(nlpruError):
    """
    Error handler for conversation building and analysis
    """
    pass

class TopicModelError(nlpruError):
    """
    Error handler for Topic modeling/by topic document categorization
    """
    pass

class InputError(nlpruError):
    """
    Error handler for improper input into the any of the library functions/objects
    """
    pass