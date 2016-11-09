"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

This file contains default complex generators of sequences.
Complex generator means that this generator returns (sequence, log) where
log's structure is depends on complex generator.

Information about sequences can be found in the sequence.py file which is contained in repository at
https://github.com/sanchousic/diploma17-test-data-generation/
"""
import random
import numpy as np


def probabilistic_generator(parameters):
    """generate complex sequence with log using different generators with matrix of probabilities

    :param parameters: (state, operations, probabilities, n) where
        state: which generator will be used in first iteration
        operations: [(sequence_generator_1, sequence_generator_parameters_1, log_num_1), ...] where
            sequence_generator: generator which gives sequence
            sequence_generator_parameters: parameters for sequence_generator
            log_num: id which will be concatenate to current log len(returned_sequence) times
        probabilities: matrix len(operations) x len(operations) != 0
        n: number of iterations
    :return: sequence, log
    """
    state, operations, probabilities, n = parameters
    sequence = []
    log = np.zeros((0,))

    def get_next_state(weights):
        """returns next state using weights"""
        random_k = random.uniform(0.0, 1.0)
        next_state = 0
        sum_of_weights = 0
        while next_state < len(weights):
            if weights[next_state] == 0:
                next_state += 1
                continue
            sum_of_weights += weights[next_state]
            if random_k < sum_of_weights:
                return next_state
            next_state += 1
        return np.argmax(weights)

    for i in range(0, n):
        op, params, log_num = operations[state]
        core_part = op(params)
        # TODO: Think of it
        sequence = sequence + list(core_part)
        log = np.concatenate((log, np.full(len(core_part), log_num)), axis=0)
        state = get_next_state(probabilities[state, :])
    return sequence, log
