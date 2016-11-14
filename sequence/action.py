"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""


def unite(parameters):
    """ unite n action's execution in one

    :param parameters: [(a1, p1) ... (an, pn)] where
        ai: action #i
        pi: parameters for action #i
    """
    for pair in parameters:
        a, p = pair
        a(p)
    return


def empty(parameters):
    """ empty action: it does nothing

    :param parameters: will be ignored
    """
    return
