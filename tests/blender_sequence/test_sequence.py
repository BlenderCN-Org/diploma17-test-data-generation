"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
import bpy
from sequence import sequence
from blender_sequence import sequence as b_sequence
import mathutils

def test_direct_object_motion():
    _object = bpy.data.objects['Sphere']
    _sequence = b_sequence.DirectObjectMotion(_object=_object,
                                              distance=2,
                                              local_direction=mathutils.Vector((0,1,0)),
                                              min_step=0.1,
                                              max_step=0.2)

    def check():
        return True

    def snapshot(index):
        print(_object.location)

    sequence.handle(_sequence, check, snapshot)
    return

def test_z_sitting_x_rotation():
    _object = bpy.data.objects['Sphere']
    _sequence = b_sequence.ZSittingXRotation(_object=_object,
                                             is_increase=True,
                                             limit_angle=90,
                                             min_d_angle=5,
                                             max_d_angle=5,
                                             z_level=0)

    def check():
        return True

    def snapshot(index):
        print(str(_object.location) + " " + str(_object.rotation_euler))

    sequence.handle(_sequence, check, snapshot)
    return
