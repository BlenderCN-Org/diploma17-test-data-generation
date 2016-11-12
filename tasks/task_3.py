"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

task 3: modulate complex object's behaviour & generate images
solution: generate sequence using complex_sequence_generator.probabilistic_generator & handle it
"""
# TODO everything, add snapshot function and blender_nodes file
import math
import random

import numpy as np

import bpy
import mathutils
from blender import nodes as b_nodes
from blender_sequence import generator as b_generator
from sequence import action
from sequence import generator
from sequence import sequence
from tasks import complex_sequence_generator


def go():
    # **********
    # 1. definitions of generators
    # **********
    def no_motion(parameters):
        frames = math.floor(random.uniform(40, 60))
        return generator.action_times_with_similar_parameters((action.empty, (), frames))

    def y_forward_motion(parameters):
        _object = parameters
        direction = mathutils.Vector((0.0, 1.0, 0.0))
        length = 2
        min_speed = 0.18
        max_speed = 0.22
        return b_generator.direct_object_motion((_object, direction, length, min_speed, max_speed))

    def sit_up_motion(parameters):
        _object = parameters
        d_angle_min = 2
        d_angle_max = 3
        limit = 90
        z_level = 0
        return b_generator.z_sitting_x_rotation_motion((_object, d_angle_min, d_angle_max, limit, z_level))

    def lie_down_motion(parameters):
        _object = parameters
        d_angle_min = -3
        d_angle_max = -2
        limit = 0
        z_level = 0
        return b_generator.z_sitting_x_rotation_motion((_object, d_angle_min, d_angle_max, limit, z_level))

    # ----------
    # TODO: everything
    # ----------
    def z_rotation_motion(parameters):
        return no_motion(parameters)

    # **********
    # 2. parameters for modulation
    # **********
    probabilities = np.array([[0.3, 0.3, 0.3, 0.1, 0, 0],
                              [0.3, 0.3, 0.3, 0.1, 0, 0],
                              [0.3, 0.3, 0.3, 0.1, 0, 0],
                              [0, 0, 0, 0, 0.2, 0.8],
                              [0.3, 0.3, 0.3, 0.1, 0, 0],
                              [0, 0, 0, 0, 0.5, 0.5]],
                             dtype=np.float)

    _object = bpy.data.objects['Sphere']

    behaviour_types = ((no_motion, _object, 1),
                       (z_rotation_motion, _object, 2),
                       (y_forward_motion, _object, 3),
                       (sit_up_motion, _object, 4),
                       (lie_down_motion, _object, 5),
                       (no_motion, _object, 6))

    init_state = 0
    number_of_iterations = 10

    # **********
    # 3. modulation
    # **********
    _sequence, journal = complex_sequence_generator.probabilistic_generator(
        (init_state, behaviour_types, probabilities, number_of_iterations))

    # **********
    # 4. init nodes
    # **********
    b_nodes.init_for_z_depth_with_noise((-3, 1 / 7.0, True, 0.0, True, 1.0))

    # **********
    # 5. handle sequence
    # **********
    def render_and_save_image_from_viewer_node(dir_path, prefix_name, index):
        file_path = str(dir_path) + str(prefix_name) + "_" + str(index).zfill(4) + ".png"
        bpy.ops.render.render()
        bpy.data.images['Viewer Node'].save_render(filepath=file_path)
        return

    def snapshot_function(index):
        dir_path = '/Users/alexmenkin/Documents/seventh column/diploma/output/task 4/point 1/'
        prefix_name = 'image'
        render_and_save_image_from_viewer_node(dir_path, prefix_name, index)
        return

    sequence.handle(_sequence, snapshot_function)
