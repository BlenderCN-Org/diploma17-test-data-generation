"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
from sequence import sequence


def test_action_n_times_with_similar_parameters():
    """ test ActionNTimesWithSimilarParameters """
    a = [0]
    def a_action(parameters):
        a = parameters
        a[0] += 1
    _sequence = sequence.ActionNTimesWithSimilarParameters(a_action, a, 10)
    def snapshot(index):
        print(a[0])
    def check():
        return True
    result = sequence.handle(_sequence, check, snapshot)
    print(result)
    return


def test_action_n_times_with_differnt_parameters():
    """ test ActionNTimesWithDifferentParameters """
    a = [0,0,0,0,0]
    p = [(a, 0), (a, 1), (a, 2), (a, 3), (a, 4)]
    def a_action(parameters):
        a, ind = parameters
        a[ind] += 1
    _sequence = sequence.ActionNTimesWithDifferentParameters(a_action, p)
    def snapshot(index):
        print(a)
    def check():
        return True
    result = sequence.handle(_sequence, check, snapshot)
    print(result)
    return


def test_unite_parameters():
    """ test ActionNTimesWithSimilarParameters """
    a = [0, 0]

    def a_action(parameters):
        a = parameters
        a[0] += 1
    def b_action(parameters):
        a = parameters
        a[1] += 1
    _sequences = [sequence.ActionNTimesWithSimilarParameters(a_action, a, 5),
                  sequence.ActionNTimesWithSimilarParameters(b_action, a, 5)]
    _sequence = sequence.Unite(_sequences)
    def snapshot(index):
        print(a)
    def check():
        return True
    result = sequence.handle(_sequence, check, snapshot)
    print(result)
    return


def test_handles_check():
    a = [0]
    def a_action(parameters):
        a = parameters
        a[0] += 1
    _sequence = sequence.ActionNTimesWithSimilarParameters(a_action, a, 10)
    def snapshot(index):
        print(a[0])
    def check():
        return a[0] < 6
    result = sequence.handle(_sequence, check, snapshot)
    print(result)
    return