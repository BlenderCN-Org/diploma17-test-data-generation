"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be 
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

This file contains a set of functions for work with sequence.
Sequence is an array of pairs.
Pair is a tuple (action, parameters) created for action(parameters) execution
Snapshot_function: function with type: function(parameter: int): void

Information about actions can be found in the sequence.action.py at
https://github.com/sanchousic/diploma17-test-data-generation/blob/master/sequence/action.py
"""


def handle(sequence, snapshot_function):
    """ execute actions one by one with "making a snapshot" after every one

    :param sequence: [pair_1 ... pair_n] where
        pair_i is a (action, action_parameters)
    :param snapshot_function: function(parameter: int): void which is called after every action's execution
    """
    index = 0
    for pair in sequence:
        action_function, parameters = pair
        action_function(parameters)
        snapshot_function(index)
        index += 1
    return
