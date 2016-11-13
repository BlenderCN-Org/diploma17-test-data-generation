"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

This file contains sequence generators for task 2
"""
import math
import random
import mathutils
from sequence import action as action
from sequence import generator as generator
from blender_sequence import action as b_action
from blender_sequence import generator as b_generator


# for 1, 5
def no_motion(parameters):
    min_frames, max_frames = parameters
    frames = math.floor(random.uniform(min_frames, max_frames))
    return generator.action_times_with_similar_parameters((action.empty, (), frames))


# for 2
def y_forward_motion(parameters):
    _object, min_length, max_length, min_speed, max_speed = parameters
    direction = mathutils.Vector((0.0, 1.0, 0.0))
    length = random.uniform(min_length, max_length)
    return b_generator.direct_object_motion((_object, direction, length, min_speed, max_speed))


# for 6
def x_back_motion(parameters):
    _object, min_length, max_length, min_speed, max_speed = parameters
    direction = mathutils.Vector((-1.0, 0.0, 0.0))
    length = random.uniform(min_length, max_length)
    return b_generator.direct_object_motion((_object, direction, length, min_speed, max_speed))


# for 3, 7
def z_rotation_motion(parameters):
    _object, min_angle, max_angle, min_speed, max_speed = parameters
    angle = random.uniform(min_angle, max_angle)
    if random.choice([True, False]):
        angle *= -1
        min_speed *= -1
        max_speed *= -1
    current_angle = 0
    generated_parameters = []
    while True:
        diff = random.uniform(min_speed, max_speed)
        generated_parameters.append((_object, diff))
        current_angle += diff
        if angle > 0:
            if current_angle >= angle:
                break
        else:
            if current_angle <= angle:
                break
    return generator.action_n_times_with_different_parameters((b_action.change_rotation_z, generated_parameters))


# for 4, 8
def sitting_up_lying_down(parameters):
    _object, min_speed, max_speed = parameters
    limit = 90
    if min_speed < max_speed < 0:
        limit = 0
    return b_generator.z_sitting_x_rotation_motion((_object, min_speed, max_speed, limit, 0))
