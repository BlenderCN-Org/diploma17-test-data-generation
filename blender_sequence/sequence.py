"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
from sequence import sequence
from blender_sequence import action as b_action
import mathutils
import numpy as np
import math
import random


class DirectObjectMotion:
    def __init__(self, _object, local_direction, distance, min_step, max_step):
        self._object = _object
        self._local_direction = local_direction
        self._distance = distance
        self._min_step = min_step
        self._max_step = max_step
        self._way = 0
        self._global_direction = np.zeros((0,))
        return
    def execute(self):
        if not self.check():
            return
        if self._way == 0:
            mat = self._object.matrix_world.copy()
            direction = mat * self._local_direction - mat * mathutils.Vector((0, 0, 0))
            scale_x = self._object.scale.x
            scale_y = self._object.scale.y
            scale_z = self._object.scale.z
            direction = np.array([direction[0], direction[1], direction[2]]) / np.array([scale_x, scale_y, scale_z])
            self._global_direction = direction / math.sqrt(direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2])
        step = random.uniform(self._min_step, self._max_step)
        offset = self._global_direction * step
        b_action.change_location((self._object, offset[0], offset[1], offset[2]))
        self._way += step
        return
    def check(self):
        return self._way < self._distance

class ZSittingXRotation:
    def __init__(self, _object, limit_angle, is_increase, min_d_angle, max_d_angle, z_level):
        self._object = _object
        self._limit_angle = limit_angle
        self._is_increase = is_increase
        min_d_angle = math.fabs(min_d_angle)
        max_d_angle = math.fabs(max_d_angle)
        if not self._is_increase:
            min_d_angle *= -1
            max_d_angle *= -1
        if min_d_angle > max_d_angle:
            min_d_angle, max_d_angle = max_d_angle, min_d_angle
        self._min_d_angle = min_d_angle
        self._max_d_angle = max_d_angle
        self._z_level = z_level
        return
    def execute(self):
        if self.check():
            d_angle = random.uniform(self._min_d_angle, self._max_d_angle)
            b_action.z_sitting_x_rotation((self._object, d_angle, self._limit_angle, self._z_level))
        return
    def check(self):
        if self._is_increase:
            return self._object.rotation_euler.x < self._limit_angle
        else:
            return self._object.rotation_euler.x > self._limit_angle
