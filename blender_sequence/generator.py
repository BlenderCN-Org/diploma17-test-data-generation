"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

This file contains default generators of sequences specified for blender.

Information about sequences can be found in the sequence.py file at
https://github.com/sanchousic/diploma17-test-data-generation/blob/master/sequence/sequence.py
"""
import math
import random
import mathutils

import numpy as np

from blender_sequence import action


# TODO: everything
def direct_object_motion(parameters):
    """ generate sequence of direct movements of blender's object with direction in its coordinates

    :param parameters: (_object, direction, length, min_speed, max_speed) where
        _object: blender's object
        direction: 3-dimensional mathutils.Vector
        length: length of motion
        min_speed: min length of motion per iteration
        max_speed: max length of motion per iteration
    :return: sequence
    """
    _object, direction, length, min_speed, max_speed = parameters
    way = 0
    sequence = []
    mat = _object.matrix_world.copy()
    direction = mat * direction - mat * mathutils.Vector((0, 0, 0))
    scale_x = _object.scale.x
    scale_y = _object.scale.y
    scale_z = _object.scale.z
    direction = np.array([direction[0], direction[1], direction[2]]) / np.array([scale_x, scale_y, scale_z])
    direction = direction / math.sqrt(direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2])
    while way < length:
        speed = random.uniform(min_speed, max_speed)
        if way + speed > length:
            speed = length - way
        offset = direction * speed
        print(direction)
        _action = action.change_location
        action_parameters = (_object, offset[0], offset[1], offset[2])
        sequence.append((_action, action_parameters))
        _action(action_parameters)
        way += speed
    return sequence


# TODO: everything
def z_sitting_x_rotation_motion(parameters):
    """ generate sequence which rotates blender's object along x-axis and moves along z-axis to make its
    the lowest point's z-coordinate equal level_z

    :param parameters:
        _object: blender object
        min_d_angle: min difference of angle in rotation per frame in degrees
        max_d_angle: max difference of angle in rotation per frame in degrees
        limit: final angle
        level_z: meaning for z coordinate of the lowest point of object
    :return: sequence
    """
    _object, d_angle_min, d_angle_max, limit, level_z = parameters
    sequence = []
    current_angle = math.degrees(_object.rotation_euler.x)
    while True:
        if d_angle_min > 0 and current_angle >= limit:
            break
        if d_angle_max < 0 and current_angle <= limit:
            break
        d_angle = random.uniform(d_angle_min, d_angle_max)
        _action = action.z_sitting_x_rotation
        action_parameters = (_object, d_angle, limit, level_z)
        sequence.append((_action, action_parameters))
        _action(action_parameters)
        current_angle += d_angle
    return sequence
