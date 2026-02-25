"""
Helper functions for Boggle game.
"""



def boggle_chars(text):
    """Yield characters from text, combining 'q' and following 'u' into 'qu'.

    Raises ValueError if 'q' appears without a following 'u'.

    >>> list(boggle_chars("quiet"))
    ['qu', 'i', 'e', 't']
    >>> list(boggle_chars("disqualify"))
    ['d', 'i', 's', 'qu', 'a', 'l', 'i', 'f', 'y']
    """
    it = iter(text)
    for char in it:
        if char == "q":
            following = next(it, None)
            if following != "u":
                raise ValueError("'Q' without a 'u'.")
            yield "qu"
        else:
            yield char