"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be 
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""

# TODO: handle function
def handle(sequence, check, snapshot):
    """ handle sequence

    :param sequence: object with methods:
        execute(): void
        check(): boolean
    :param check: check(): boolean
    :param snapshot: snapshot(index: int): void
    :return: &(i = 1..n) check()
    """
    i = 0
    while sequence.check():
        sequence.execute()
        if not check():
            return False
        snapshot(i)
        i += 1
    return True

class ActionNTimesWithSimilarParameters:
    def __init__(self, action, parameters, n):
        self._action = action
        self._parameters = parameters
        self._n = n
        self._i = 0
        return
    def execute(self):
        if self.check():
            self._action(self._parameters)
            self._i += 1
        return
    def check(self):
        return self._i < self._n

class ActionNTimesWithDifferentParameters:
    def __init__(self, action, array_of_parameters):
        self._action = action
        self._array_of_parameters = array_of_parameters
        self._i = 0
        return
    def execute(self):
        if self.check():
            self._action(self._array_of_parameters[self._i])
            self._i += 1
        return
    def check(self):
        return self._i < len(self._array_of_parameters)

class Unite:
    def __init__(self, sequences):
        self._sequences = sequences
        self._i = 0
        return
    def execute(self):
        if self.check():
            self._sequences[self._i].execute()
        return
    def check(self):
        while self._i < len(self._sequences):
            if self._sequences[self._i].check():
                return True
            else:
                self._i += 1
        return False
