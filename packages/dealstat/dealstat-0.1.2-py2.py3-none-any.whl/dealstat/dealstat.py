# -*- coding: utf-8 -*-

"""Main module."""

import random, string

# STANDARD IMPORTS
def unique_id():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(25))


def compare_figures(figure1, figure2, thresh = 0.99):
    if figure1 == figure2:
        return True
    elif figure1 >= figure2 and figure1 * thresh <= figure2:
        return True
    elif figure2 >= figure1 and figure2 * thresh <= figure1:
        return True
    else:
        return False
