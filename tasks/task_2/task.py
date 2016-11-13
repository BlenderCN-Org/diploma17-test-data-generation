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
from sequence import sequence
from tasks import blender_nodes as b_nodes
from tasks.task_2 import complex_generator
from tasks.task_2 import generator as t_generator


def go():
    """ Task 2 """
    _object = bpy.data.objects['Sphere']

    """ operations

    operations:
        1. lying - static:              no_motion
        2. lying - forward motion:      y_forward_motion
        3. lying - rotation:            z_rotation_motion
        4. sitting up:                  sitting_up_lying_down
        5. sitting - static:            no_motion
        6. sitting - forward motion:    x_back_motion
        7. sitting - rotation:          z_rotation_motion
        8. lying down:                  sitting_up_lying_down

    generators:
        1. no_motion(min_frames, max_frames)
        2. y_forward_motion(_object, min_length, max_length, min_speed, max_speed)
        3. x_back_motion(_object, min_length, max_length, min_speed, max_speed)
        4. z_rotation_motion(_object, min_angle, max_angle, min_speed, max_speed)
        5. sitting_up_lying_down(_object, min_speed, max_speed)
    """
    operations = ((t_generator.no_motion,               (20, 40),                           1),
                  (t_generator.y_forward_motion,        (_object, 2, 3, 0.1, 0.25),         2),
                  (t_generator.z_rotation_motion,       (_object, 20, 40, 2, 3),            3),
                  (t_generator.sitting_up_lying_down,   (_object, 2, 3),                    4),
                  (t_generator.no_motion,               (20, 40),                           5),
                  (t_generator.x_back_motion,           (_object, 1, 2.5, 0.05, 0.2),       6),
                  (t_generator.z_rotation_motion,       (_object, 20, 40, 2, 4),            5),
                  (t_generator.sitting_up_lying_down,   (_object, -4, -2),                  7))

    probabilities = np.array([[0.4,  0.2,  0.2, 0.2, 0,    0,    0,   0  ],
                              [0.2,  0.3,  0.3, 0.2, 0,    0,    0,   0  ],
                              [0.2,	 0.2,  0.4, 0.2, 0,    0,    0,   0  ],
                              [0,    0,    0,   0,   0.45, 0.45, 0.1, 0  ],
                              [0,    0,    0,   0,   0.2,  0.4,  0.1, 0.3],
                              [0,    0,    0,   0,   0.2,  0.1,  0.3, 0.4],
                              [0,    0,    0,   0,   0.1,  0.2,  0.2, 0.5],
                              [0.45, 0.45, 0.1, 0,   0,    0,    0,   0  ]],
                             dtype=np.float)
    journal = []
    transforms = []
    n = 1

    def init():

        # scale
        scale_x = random.uniform(0.2, 0.3)
        scale_y = random.uniform(0.5, 0.7)
        scale_z = random.uniform(scale_x - 0.05, scale_x + 0.05)
        location_x = random.uniform(-1, 1)
        location_y = random.uniform(-1, 1)
        rotation_y = math.radians(0.0)
        rotation_z = random.uniform(math.radians(0), math.radians(360))

        random_k = random.uniform(0.0, 1.0)
        location_z = scale_z
        rotation_x = math.radians(0.0)
        state = random.choice([0, 1, 2, 3])
        if random_k > 0.75:
            location_z = scale_y
            rotation_x = math.radians(90.0)
            state = random.choice([4, 5, 6, 7])

        return state, ((location_x, location_y, location_z),
                       (rotation_x, rotation_y, rotation_z),
                       (scale_x, scale_y, scale_z))

    # main part
    for i in range(n):
        init_state, transform = init()
        transforms.append(transform)
        performances = 10
        parameters = (init_state, operations, probabilities, performances)
        journal.append(complex_generator.probabilistic_generator(parameters))

    # init nodes
    b_nodes.init_for_z_depth_with_noise(count_z_depth_parameters(15, 3, 0))

    for i in range(n):
        def snapshot_function(index):
            generate_image(i + 1, index)
            return
        _sequence, log = journal[i]
        _object.location = transforms[i][0]
        _object.rotation_euler = transforms[i][1]
        _object.scale = transforms[i][2]
        print(log)
        sequence.handle(_sequence, snapshot_function)
        # TODO save log

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
