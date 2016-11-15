"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
import random
import numpy as np


class ProbabilisticComplexSequence:
    def __init__(self, state, generators, logs, probabilities, performances):
        self._state = state
        self._generators = generators
        self._logs = logs
        self._probabilities = probabilities
        self._performances = performances
        self._i = 0
        self._sequence = self._generators[self._state].get_sequence()
        self.logs_note = []
        return
    def execute(self):
        if self.check():
            self._sequence.execute()
            self.logs_note.append(self._logs[self._state])
        return
    def check(self):
        while self._i < self._performances:
            if self._sequence.check():
                return True
            else:
                self._state = self._get_next_state()
                self._sequence = self._generators[self._state].get_sequence()
                self._i += 1
        return False
    def _get_next_state(self):
        weights = self._probabilities[self._state, :]
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