import bpy
from random import uniform

def reset_scene():
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

    collections = [col.name for col in bpy.data.collections]
    for name in collections:
        bpy.data.collections.remove(bpy.data.collections[name])

    # bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)


def make_cube(location, scale, name, mesh):
    cube = bpy.data.objects.new(name=name, object_data=mesh)
    cube.scale = scale
    cube.location = location
    r = uniform(0.0, 1.0)
    g = uniform(0.0, 1.0)
    b = uniform(0.0, 1.0)
    cube['primary_color'] = (r, g, b)
    bpy.data.collections[name].objects.link(cube)


def create_building_corner_posts(x, y, building_width, base_width, start_height, building_height, mesh):
    for xm, ym in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        xc = x + xm * building_width / 2.0
        yc = y + ym * building_width / 2.0
        post_width = (base_width - building_width) / 3.0

        make_cube((xc, yc, start_height + building_height / 2), (post_width, post_width, building_height), 'building', mesh)


def create_building_base(xl, yl, start_height, base_height, base_width, mesh):
    make_cube((xl, yl, start_height + base_height / 2), (base_width, base_width, base_height), 'building', mesh)


def create_building_segment(x, y, start_height, width_min, width_max, templates):
    z = uniform(0.5, 3.0)
    zh = z / 2

    width = uniform(width_min, width_max)
    base_width = width * 1.2
    base_height = uniform(0.1, 0.2)

    # create the base
    create_building_base(x, y, start_height, base_height, base_width, templates['building_base'])

    make_cube((x, y, zh + base_height + start_height), (width, width, z), 'building', templates['building_windows'])
    # create the top base

    create_building_base(x, y, z + base_height + start_height, base_height, base_width, templates['building_base'])

    create_building_corner_posts(x, y, width, base_width, base_height + start_height, z, templates['building_base'])

    return base_height * 2 + start_height + z, width


def create_building(x, y, num_segments, templates):
    top = 0.0
    width = 1.1
    for i in range(num_segments):
        top, width = create_building_segment(x, y, top, width * 0.8,
                                             width * 1.1, templates)
    return top

def create_templates():

    templates = {}

    materials = bpy.data.materials
    collection = bpy.data.collections.new("building")
    bpy.context.scene.collection.children.link(collection)

    bpy.ops.mesh.primitive_cube_add(size=1)
    building_windows = bpy.context.object
    building_windows.data.materials.append(materials['building_wall'])
    mesh = building_windows.data
    templates['building_windows'] = mesh
    building_windows.hide_render = True
    building_windows.hide_viewport = True

    bpy.ops.mesh.primitive_cube_add(size=1)
    building_base = bpy.context.object
    building_base.data.materials.append(materials['building_base'])
    mesh = building_base.data
    templates['building_base'] = mesh
    building_base.hide_render = True
    building_base.hide_viewport = True
    return templates

def create_scene():

    templates = create_templates()
    for y in range(-10, 2, 2):
        for x in range(0, 4, 4):
            if uniform(0.0, 1.0) < 0.8:
                yo = uniform(-1.0, 1.0) + y
                xo = uniform(-0.5, 0.5) + x
                top = create_building(xo, yo, 4, templates)



def blender():
    print ('generating art!')
    reset_scene()
    create_scene()

