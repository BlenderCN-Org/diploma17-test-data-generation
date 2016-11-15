"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
from sequence import sequence
import numpy as np
from tasks.task_2 import complex_sequence

def test_probabilistic_complex_sequence():
    def foo(parameters):
        print(parameters)
        return
    class TestGenerator:
        def __init__(self, num, length):
            self._num = num
            self._len = length
            return
        def get_sequence(self):
            return sequence.ActionNTimesWithSimilarParameters(foo, self._num, self._len)
    a = TestGenerator(1, 1)
    b = TestGenerator(2, 2)
    c = TestGenerator(3, 3)
    logs = [1, 2, 3]
    probabilities = np.array([[0, 0.5, 0.5], [0.2, 0, 0.8], [0.5, 0.5, 0]])
    _sequence = complex_sequence.ProbabilisticComplexSequence(0, [a, b, c], logs, probabilities, 10)
    def snapshot(index):
        return
    def check():
        return True
    sequence.handle(_sequence, check, snapshot)
    print(_sequence.logs_note)
    return