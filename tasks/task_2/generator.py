"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
import math
import random
from sequence import action
from sequence import sequence
from blender_sequence import action as b_action
from blender_sequence import sequence as b_sequence


class NoMotion:
    def __init__(self, min_frames, max_frames):
        if min_frames > max_frames:
            min_frames, max_frames = max_frames, min_frames
        self._min_frames = min_frames
        self._max_frames = max_frames
        return
    def get_sequence(self):
        frames = random.uniform(self._min_frames, self._max_frames)
        return sequence.ActionNTimesWithSimilarParameters(action.empty, (), frames)

class DirectObjectMotionGenerator:
    def __init__(self, _object, local_direction, distance, min_step, max_step):
        self._object = _object
        self._distance = distance
        self._min_step = min_step
        self.max_step = max_step
        self._local_direction = local_direction
        return

    def get_sequence(self):
        return b_sequence.DirectObjectMotion(self._object, self._local_direction, self._distance, self._min_step,
                                             self.max_step)

class ZRotationMotion:
    def __init__(self, _object, min_angle, max_angle, min_d_angle, max_d_angle):
        self._object = _object

        min_angle = math.fabs(min_angle)
        max_angle = math.fabs(max_angle)
        if min_angle > max_angle:
            min_angle, max_angle = max_angle, min_angle
        self._min_abs_angle = min_angle
        self._max_abs_angle = max_angle

        min_d_angle = math.fabs(min_d_angle)
        max_d_angle = math.fabs(max_d_angle)
        if min_d_angle > max_d_angle:
            min_d_angle, max_d_angle = max_d_angle, min_d_angle
        self._min_abs_d_angle = min_d_angle
        self._max_abs_d_angle = max_d_angle

        return

    def get_sequence(self):

        min_angle = self._min_abs_angle
        max_angle = self._max_abs_angle
        min_d_angle = self._min_abs_d_angle
        max_d_angle = self._max_abs_d_angle

        is_increase = random.choice([True, False])
        if not is_increase:
            min_d_angle, max_d_angle = max_d_angle * -1, min_d_angle * -1
            min_angle, max_angle = max_angle * -1, min_angle * -1

        limit_angle = random.uniform(min_angle, max_angle)
        angle = 0
        array_of_action_parameters = []
        while is_increase and angle < limit_angle or not is_increase and angle > limit_angle:
            d_angle = random.uniform(min_d_angle, max_d_angle)
            array_of_action_parameters.append((self._object, d_angle))
            angle += d_angle

        return sequence.ActionNTimesWithDifferentParameters(b_action.change_rotation_z, array_of_action_parameters)

class ZeroZSittingXRotation:
    def __init__(self, _object, limit_angle, is_increase, min_d_angle, max_d_angle):
        self._object = _object
        self._limit_angle = limit_angle
        self._is_increase = is_increase
        self._min_d_angle = min_d_angle
        self._max_d_angle = max_d_angle
        self._z_level = 0
        return

    def get_sequence(self):
        return b_sequence.ZSittingXRotation(self._object, self._limit_angle, self._is_increase, self._min_d_angle,
                                            self._max_d_angle, self._z_level)
