"""
Copyright (c) 2016 Alexandr Menkin 
Use of this source code is governed by an MIT-style license that can be  
found in the LICENSE file at https://github.com/sanchousic/diploma17-test-data-generation/blob/master/LICENSE

This file contains a set of functions for work with blender's nodes.
"""
import bpy


"""
How does z_depth count value using parameters (offset, size, use_min, min, use_max, max):
distance = distance to nearest not empty point on scene
result = size * distance + offset
if use_max and result > max then result = max
if use_min and result < min then result = min
"""


def init_for_z_depth(parameters):
    """build nodes to get images of z_depth channel

    :param parameters: (offset, size, use_min, min, use_max, max)
        offset: float
        size: float
        use_min: bool
        min: float
        use_max: bool
        max: float
    """
    offset, size, use_min, _min, use_max, _max = parameters
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links
    for n in tree.nodes:
        tree.nodes.remove(n)

    r_layers_node = tree.nodes.new('CompositorNodeRLayers')
    r_layers_node.location = 0, 200
    r_layers_node.scene = bpy.data.scenes["Scene"]

    composite_node = tree.nodes.new('CompositorNodeComposite')
    composite_node.location = 200, 200
    links.new(r_layers_node.outputs['Image'], composite_node.inputs['Image'])

    map_value_node = tree.nodes.new('CompositorNodeMapValue')
    map_value_node.offset[0] = offset
    map_value_node.size[0] = size
    map_value_node.use_min = use_min
    map_value_node.min[0] = _min
    map_value_node.use_max = use_max
    map_value_node.max[0] = _max
    map_value_node.location = 200, 0
    links.new(r_layers_node.outputs['Z'], map_value_node.inputs['Value'])

    invert_node = tree.nodes.new('CompositorNodeInvert')
    invert_node.location = 400, 0
    links.new(map_value_node.outputs['Value'], invert_node.inputs['Color'])

    viewer_node = tree.nodes.new('CompositorNodeViewer')
    viewer_node.location = 600, 0
    links.new(invert_node.outputs['Color'], viewer_node.inputs['Image'])
    return


def init_for_z_depth_with_noise(parameters):
    """build nodes to get images of z_depth channel with noise

    :param parameters: (offset, size, use_min, min, use_max, max)
        offset: float
        size: float
        use_min: bool
        min: float
        use_max: bool
        max: float
    """
    offset, size, use_min, _min, use_max, _max = parameters
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links
    for n in tree.nodes:
        tree.nodes.remove(n)

    r_layers_node = tree.nodes.new('CompositorNodeRLayers')
    r_layers_node.location = 0, 200
    r_layers_node.scene = bpy.data.scenes["Scene"]

    composite_node = tree.nodes.new('CompositorNodeComposite')
    composite_node.location = 200, 200
    links.new(r_layers_node.outputs['Image'], composite_node.inputs['Image'])

    map_value_node = tree.nodes.new('CompositorNodeMapValue')
    map_value_node.offset[0] = offset
    map_value_node.size[0] = size
    map_value_node.use_min = use_min
    map_value_node.min[0] = _min
    map_value_node.use_max = use_max
    map_value_node.max[0] = _max
    map_value_node.location = 200, 0
    links.new(r_layers_node.outputs['Z'], map_value_node.inputs['Value'])

    texture_node = tree.nodes.new('CompositorNodeTexture')
    texture_node.texture = bpy.data.textures['Texture']
    texture_node.location = 0, -300
    texture_node.inputs[0].default_value = (10, 2, 5)
    blur_node = tree.nodes.new('CompositorNodeBlur')
    blur_node.inputs[1].default_value = 0.5
    blur_node.location = 200, -300
    links.new(texture_node.outputs['Color'], blur_node.inputs['Image'])
    mix_node = tree.nodes.new('CompositorNodeMixRGB')
    mix_node.blend_type = 'OVERLAY'
    mix_node.inputs[0].default_value = 0.1
    mix_node.location = 600, 0
    links.new(map_value_node.outputs['Value'], mix_node.inputs[1])
    links.new(blur_node.outputs['Image'], mix_node.inputs[2])

    viewer_node = tree.nodes.new('CompositorNodeViewer')
    viewer_node.location = 800, 0
    links.new(mix_node.outputs['Image'], viewer_node.inputs['Image'])
    return


def render_and_save_image_from_viewer_node(dir_path, prefix_name, index, extension):
    """ this function renders and saves image from viewer node
    with path: 'dir_path + prefix_name + number + . + format' where number is from 0000 to 9999

    :param dir_path: string: with slash in the end
    :param prefix_name: the first part of file's name
    :param index: int: number, the last part of file's name, it should be 0..9999
    :param extension: extension of file without '.', for example: 'png'
    """
    file_path = dir_path + str(prefix_name) + str(index).zfill(4) + '.' + extension
    bpy.ops.render.render()
    bpy.data.images['Viewer Node'].save_render(filepath=file_path)
    return