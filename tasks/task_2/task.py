"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

Task 2
Destination: modulate complex object's behaviour & generate images
Parameters:
    resolution: 320 x 240
    fov: 62 x 48.6 degrees
    space d: 550 mm
    camera z: 1500 mm
"""
import bpy
import numpy as np
import random
import math
import mathutils
from blender_sequence import action as b_action
from sequence import sequence
from tasks import blender_nodes as b_nodes
from tasks.task_2 import complex_sequence
from tasks.task_2 import generator as t_generator


def go():
    """ Main function for task 2"""

    # ellipsoid
    _object = bpy.data.objects['Sphere']


    # generators
    no_motion = t_generator.NoMotion(min_frames=20,
                                     max_frames=40)

    lying_forward_motion = t_generator.DirectObjectMotionGenerator(_object=_object,
                                                                   local_direction=mathutils.Vector((0, 1, 0)),
                                                                   distance=1.5,
                                                                   min_step=0.1,
                                                                   max_step=0.3)

    sitting_forward_motion = t_generator.DirectObjectMotionGenerator(_object=_object,
                                                                     local_direction=mathutils.Vector((0, 1, 0)),
                                                                     distance=1,
                                                                     min_step=0.1,
                                                                     max_step=0.2)

    sitting_z_rotation = t_generator.ZRotationMotion(_object=_object,
                                                     min_angle=30,
                                                     max_angle=60,
                                                     min_d_angle=2,
                                                     max_d_angle=3)

    lying_z_rotation = t_generator.ZRotationMotion(_object=_object,
                                                   min_angle=20,
                                                   max_angle=40,
                                                   min_d_angle=1.5,
                                                   max_d_angle=2)

    sitting_up = t_generator.ZeroZSittingXRotation(_object=_object,
                                                   limit_angle=90,
                                                   is_increase=True,
                                                   min_d_angle=2,
                                                   max_d_angle=3)

    lying_down = t_generator.ZeroZSittingXRotation(_object=_object,
                                                   limit_angle=0,
                                                   is_increase=False,
                                                   min_d_angle=-3,
                                                   max_d_angle=-2)


    # ProbabilisticComplexSequence
    generators = [no_motion,
                  lying_forward_motion,
                  lying_z_rotation,
                  sitting_up,
                  no_motion,
                  sitting_forward_motion,
                  sitting_z_rotation,
                  lying_down]

    logs = [1, 2, 3, 4, 5, 6, 5, 7]

    probabilities = np.array([[0.4, 0.2, 0.2, 0.2, 0, 0, 0, 0],
                              [0.2, 0.3, 0.3, 0.2, 0, 0, 0, 0],
                              [0.2, 0.2, 0.4, 0.2, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0.45, 0.45, 0.1, 0],
                              [0, 0, 0, 0, 0.2, 0.4, 0.1, 0.3],
                              [0, 0, 0, 0, 0.2, 0.1, 0.3, 0.4],
                              [0, 0, 0, 0, 0.1, 0.2, 0.2, 0.5],
                              [0.45, 0.45, 0.1, 0, 0, 0, 0, 0]],
                             dtype=np.float)

    def init():
        # scale
        scale_x = random.uniform(0.1, 0.15)
        scale_y = random.uniform(0.25, 0.35)
        scale_z = random.uniform(scale_x - 0.025, scale_x + 0.025)
        location_x = random.uniform(-1, 1)
        location_y = random.uniform(-1, 1)
        rotation_y = math.radians(0.0)
        rotation_z = random.uniform(math.radians(0), math.radians(360))
        location_z = scale_z
        rotation_x = math.radians(0.0)
        state = random.choice([0, 1, 2, 3])
        if random.choice([True, False]):
            location_z = scale_y
            rotation_x = math.radians(90.0)
            state = random.choice([4, 5, 6, 7])
        b_action.set_location((_object, location_x, location_y, location_z))
        b_action.set_rotation((_object, rotation_x, rotation_y, rotation_z))
        _object.scale = (scale_x, scale_y, scale_z)
        return state

    # prepare for sequence's host
    journal = []
    n_modulation = 2
    performances_per_modulation = 10

    def check():
        x = _object.location.x
        y = _object.location.y
        return (-8.5 < x < 8.5)  and (-6.2 < y < 6.2)

    # init nodes
    b_nodes.init_for_z_depth_with_noise(count_z_depth_parameters(15, 3, 0))

    # main part
    for i in range(n_modulation):
        init_state = init()
        pcs = complex_sequence.ProbabilisticComplexSequence(init_state, generators, logs, probabilities, performances_per_modulation)

        def snapshot(index):
            #generate_image(i, index)
            return

        sequence.handle(pcs, check, snapshot)
        journal.append(pcs.logs_journal)
        print("")
        print(journal[i])


    return


def count_z_depth_parameters(camera, one, zero):
    """ count parameters for initialization of nodes

    :param camera: < camera
    :param one: 0 < one < camera
    :param zero: 0 < zero < camera
    :return: (offset, size, use_min, min, use_max, max)
    """
    offset =  - (camera - one)
    size = 1.0 / (one - zero)
    return (offset, size, True, 0, True, 1)


def generate_image(dir_index, index):
    dir_path = '/Users/alexmenkin/Documents/seventh column/diploma/output/task_2/' + str(dir_index).zfill(4) + '/'
    prefix_name = 'image'
    b_nodes.render_and_save_image_from_viewer_node(dir_path, prefix_name, index + 1, 'png')
    return
