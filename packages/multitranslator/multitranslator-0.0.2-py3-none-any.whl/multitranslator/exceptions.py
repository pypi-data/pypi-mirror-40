"""
multitranslator.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of MultiTranslator's exceptions.
"""


class BaseClass(Exception):
    pass


class TranslateError(BaseClass):
    """Failed to translate the text/word."""
    pass


class WordNotFound(BaseClass):
    """A Word not found into specific dictionary."""
    pass


class ConnectionError(BaseClass):
    """A Connection error occurred."""
    pass
