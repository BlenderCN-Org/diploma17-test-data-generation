"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be 
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE
"""
import math
import mathutils


def change_scale_x(parameters):
    """ change scale x of blender's object if it's possible

    :param parameters: (_object, diff_x) where
        _object: blender's object
        diff_x: additive change of scale x
    """
    _object, diff_x = parameters
    test = _object.scale.x + diff_x
    if test > 0:
        _object.scale.x = test
    return


def change_scale_y(parameters):
    """ change scale y of blender's object if it's possible

    :param parameters: (_object, diff_y) where
        _object: blender's object
        diff_y: additive change of scale y
    """
    _object, diff_y = parameters
    test = _object.scale.y + diff_y
    if test > 0:
        _object.scale.y = test
    return


def change_scale_z(parameters):
    """ change scale z of blender's object if it's possible

    :param parameters: (_object, diff_z) where
        _object: blender's object
        diff_z: additive change of scale z
    """
    _object, diff_z = parameters
    test = _object.scale.z + diff_z
    if test > 0:
        _object.scale.z = test
    return


def change_scale(parameters):
    """ change scale x, y and z (separately) of blender's object if it's possible

    :param parameters: (_object, diff_x, diff_y, diff_z) where
        _object: blender's object
        diff_x: additive change of scale x
        diff_y: additive change of scale y
        diff_z: additive change of scale z
    """
    _object, diff_x, diff_y, diff_z = parameters
    change_scale_x((_object, diff_x))
    change_scale_y((_object, diff_y))
    change_scale_z((_object, diff_z))
    return


def change_rotation_x(parameters):
    """ change rotation x of blender's object

    :param parameters: (_object, diff_degree_x) where
        _object: blender's object
        diff_degree_x: additive change of rotation x in degrees
    """
    _object, diff_degree_x = parameters
    _object.rotation_euler.x += math.radians(diff_degree_x)
    return


def change_rotation_y(parameters):
    """ change rotation y of blender's object

    :param parameters: (_object, diff_degree_y) where
        _object: blender's object
        diff_degree_y: additive change of rotation y in degrees
    """
    _object, diff_degree_y = parameters
    _object.rotation_euler.y += math.radians(diff_degree_y)
    return


def change_rotation_z(parameters):
    """ change rotation z of blender's object

    :param parameters: (_object, diff_degree_z) where
        _object: blender's object
        diff_degree_z: additive change of rotation z in degrees
    """
    _object, diff_degree_z = parameters
    _object.rotation_euler.z += math.radians(diff_degree_z)
    return


def change_rotation(parameters):
    """ change rotation of blender's object

    :param parameters: (_object, diff_degree_x, diff_degree_y, diff_degree_z) where
        _object: blender's object
        diff_degree_x: additive change of rotation x in degrees
        diff_degree_y: additive change of rotation y in degrees
        diff_degree_z: additive change of rotation z in degrees
    """
    _object, degree_x, degree_y, degree_z = parameters
    change_rotation_x((_object, degree_x))
    change_rotation_y((_object, degree_y))
    change_rotation_z((_object, degree_z))
    return


def set_rotation_x(parameters):
    """ set rotation x of blender's object

    :param parameters: (_object, degree_x) where
        _object: blender's object
        degree_x: new meaning of rotation x in degrees
    """
    _object, degree_x = parameters
    _object.rotation_euler.x = math.radians(degree_x)
    return


def set_rotation_y(parameters):
    """ set rotation y of blender's object

    :param parameters: (_object, degree_y) where
        _object: blender's object
        degree_y: new meaning of rotation y in degrees
    """
    _object, degree_y = parameters
    _object.rotation_euler.y = math.radians(degree_y)
    return


def set_rotation_z(parameters):
    """ set rotation z of blender's object

    :param parameters: (_object, degree_z) where
        _object: blender's object
        degree_z: new meaning of rotation z in degrees
    """
    _object, degree_z = parameters
    _object.rotation_euler.z = math.radians(degree_z)
    return


def set_rotation(parameters):
    """ set rotation of blender's object

    :param parameters: (_object, degree_x, degree_y, degree_z) where
        _object: blender's object
        degree_x: new meaning of rotation x in degrees
        degree_y: new meaning of rotation y in degrees
        degree_z: new meaning of rotation z in degrees
    """
    _object, degree_x, degree_y, degree_z = parameters
    set_rotation_x((_object, degree_x))
    set_rotation_y((_object, degree_y))
    set_rotation_z((_object, degree_z))
    return


def change_location(parameters):
    """ change location of blender's object

    :param parameters: (_object, diff_x, diff_y, diff_z) where
        _object: blender's object
        diff_x: additive change of location x
        diff_y: additive change of location y
        diff_z: additive change of location z
    """
    _object, diff_x, diff_y, diff_z = parameters
    _object.location.x += diff_x
    _object.location.y += diff_y
    _object.location.z += diff_z
    return


def set_location(parameters):
    """ set location of blender's object

    :param parameters: (_object, x, y, z) where
        x: new meaning of location x
        y: new meaning of location y
        z: new meaning of location z
    """
    _object, x, y, z = parameters
    _object.location.x = x
    _object.location.y = y
    _object.location.z = z
    return


# TODO: check & optimize
def z_sitting_x_rotation(parameters):
    """ x-rotation with sitting on z-level

    :param parameters: (_object, da, limit, level_z)
    """
    _object, da, limit, level_z = parameters
    current_angle = math.degrees(_object.rotation_euler.x)

    # TODO: check & optimize
    def z_sit_mesh_down(parameters2):
        """ make mesh_object lowest z coordinate equals level """
        mesh_object, level = parameters2
        min_z = 9999.0
        for vertex in mesh_object.data.vertices:
            """ object vertices are in object space, translate to world space """
            v_world = mesh_object.matrix_world * mathutils.Vector((vertex.co[0], vertex.co[1], vertex.co[2]))
            if v_world[2] < min_z:
                min_z = v_world[2]
        mesh_object.location.z -= (min_z - level)
        return

    if da >= 0 and current_angle >= limit:
        return
    if da < 0 and current_angle <= limit:
        return
    new_angle = current_angle + da
    if da >= 0 and new_angle > limit:
        new_angle = limit
    if da < 0 and new_angle < limit:
        new_angle = limit
    set_rotation_x((_object, new_angle))
    z_sit_mesh_down((_object, level_z))
    return
