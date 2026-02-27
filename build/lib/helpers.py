"""
Helper functions for Boggle game.
"""


# Boggle dice configuration.
# Each list item represents a six-sided die from the Boggle game.
# The last die has "Qu" as a single face, matching the real Boggle game.
boggle_dice = [
    "aeaneg", "wngeeh", "ahspco", "lnhnrz",
    "aspffk", "tstiyd", "objoab", "owtoat",
    "iotmuc", "erttyl", "ryvdel", "toessi",
    "lreixd", "terwhv", "eiunes", ("n", "u", "i", "h", "m", "qu"),
]

def normalize_qu(text):
    """Yield characters from text, combining 'q' and following 'u' into 'qu'.

    Raises ValueError if 'q' appears without a following 'u'.

    >>> list(normalize_qu("quiet"))
    ['qu', 'i', 'e', 't']
    >>> list(normalize_qu("disqualify"))
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