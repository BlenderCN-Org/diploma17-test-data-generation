"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

This file contains default generators of sequences.

Information about sequences can be found in the sequence.py file at
https://github.com/sanchousic/diploma17-test-data-generation/blob/master/sequence/sequence.py
"""


def action_times_with_similar_parameters(parameters):
    """ generate sequence with n the same actions

    :param parameters: (action, action_parameters, length) where
        action: action function
        action_parameters: parameters for action
        length: n
    :return: sequence [(action, action_parameters), ... (action, action_parameters)] with length length
    """
    action, action_parameters, length = parameters
    sequence = []
    pair = (action, action_parameters)
    for i in range(length):
        sequence.append(pair)
    return sequence


def action_n_times_with_different_parameters(parameters):
    """ generate sequence with n the same type of actions but different in parameters for them

    :param parameters: (action, array_of_action_parameters) where
        action: action function
        array_of_action_parameters: [action_parameters_1, ... action_parameter_n] with length n where
            action_parameters_i: parameters for action on i iteration where i = 1..n
    :return: sequence [(action, action_parameters_1), ... (action, action_parameters_n)] with length length
    """
    action, array_of_action_parameters = parameters
    sequence = []
    for action_function_parameters in array_of_action_parameters:
        sequence.append((action, action_function_parameters))
    return sequence

