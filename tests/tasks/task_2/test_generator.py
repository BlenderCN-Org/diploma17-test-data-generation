"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
from tasks.task_2 import generator as t_generator
from sequence import sequence
import mathutils
import bpy
import math


def test_no_motion():
    no_motion = t_generator.NoMotion(min_frames=20,
                                     max_frames=40)
    a = [0]
    def snapshot(index):
        a[0] += 1
        return
    def check():
        return True
    sequence.handle(no_motion.get_sequence(), check, snapshot)
    print(a[0])
    return


def test_direct_object_motion_generator_1():
    _object = bpy.data.objects['Sphere']
    y_forward_motion = t_generator.DirectObjectMotionGenerator(_object=_object,
                                                                   local_direction=mathutils.Vector((0, 1, 0)),
                                                                   distance=1.5,
                                                                   min_step=0.1,
                                                                   max_step=0.3)
    def snapshot(index):
        print(_object.location)
        return
    def check():
        return True
    sequence.handle(y_forward_motion.get_sequence(), check, snapshot)
    return


def test_direct_object_motion_generator_2():
    _object = bpy.data.objects['Sphere']
    x_back_motion = t_generator.DirectObjectMotionGenerator(_object=_object,
                                                               local_direction=mathutils.Vector((-1, 0, 0)),
                                                               distance=1.5,
                                                               min_step=0.1,
                                                               max_step=0.3)
    def snapshot(index):
        print(_object.location)
        return
    def check():
        return True
    sequence.handle(x_back_motion.get_sequence(), check, snapshot)
    return


def test_z_rotation_motion():
    _object = bpy.data.objects['Sphere']
    z_rotation = t_generator.ZRotationMotion(_object=_object,
                                             min_angle=30,
                                             max_angle=60,
                                             min_d_angle=2,
                                             max_d_angle=3)
    def snapshot(index):
        print(str(math.degrees(_object.rotation_euler.x)) + " " +
              str(math.degrees(_object.rotation_euler.y)) + " " +
              str(math.degrees(_object.rotation_euler.z)))
        return
    def check():
        return True
    sequence.handle(z_rotation.get_sequence(), check, snapshot)
    return


def test_zero_z_sitting_x_rotation_1():
    _object = bpy.data.objects['Sphere']
    sitting_up = t_generator.ZeroZSittingXRotation(_object=_object,
                                                   limit_angle=90,
                                                   is_increase=True,
                                                   min_d_angle=2,
                                                   max_d_angle=3)
    def snapshot(index):
        print(_object.location)
        return
    def check():
        return True
    sequence.handle(sitting_up.get_sequence(), check, snapshot)
    return


def test_zero_z_sitting_x_rotation_2():
    _object = bpy.data.objects['Sphere']
    lying_down = t_generator.ZeroZSittingXRotation(_object=_object,
                                                   limit_angle=0,
                                                   is_increase=False,
                                                   min_d_angle=-3,
                                                   max_d_angle=-2)
    def snapshot(index):
        print(_object.location)
        return
    def check():
        return True
    sequence.handle(lying_down.get_sequence(), check, snapshot)
    return