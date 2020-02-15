# Blender script to create QR code STLs
import bpy
import bmesh
import os
from math import sqrt

svg_path = 'files/qr.svg' # path to QR code SVG
icon_path = 'files/wifi.svg' # path to icon SVG
output_path = 'qr.stl' # path to place resulting STL

icon_radius = 0.015 # how much space you want in the center of the QR code for the icon, <= 0 for no space 

qr_height = 2.5 # height in mm of the 'black' part
icon_height = 2.5 # height in mm of the center icon
base_height = 2.5 # height in mm of the base ('white')

qr_length = 90 # length in mm of the QR code part
icon_length = 18 # length in mm of the icon
base_length = 100 # length in mm of the base

multi = False # experimental feature for multimaterial printers

# used for clearing the center of QRness
def get_distance(p1,p2):
    distance = sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
    # print(distance)  # print distance to console, DEBUG
    return distance

# delete default Blender objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# import SVG
bpy.ops.import_curve.svg(filepath=svg_path)

# select all SVG curves
bpy.ops.object.select_all(action='SELECT')
objects = bpy.context.scene.objects
bpy.context.view_layer.objects.active = objects[0]

# convert curves to mesh
bpy.ops.object.convert(target='MESH')

# join all meshes
bpy.ops.object.join()

# reset object origin (useful for scaling and keeping things centered)
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')

# resize based on qr_length
qr_scale = qr_length / bpy.context.active_object.dimensions[0]
bpy.context.active_object.scale = (qr_scale, ) * 3

# switch to edit mode, select all faces, convert tris to quads
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.tris_convert_to_quads()

# remove doubled vertices
bpy.ops.mesh.remove_doubles()

# delete faces at center to make room for icon
bpy.ops.object.editmode_toggle()

bm = bmesh.new()
bm.from_mesh(bpy.context.object.data)

bm.faces.ensure_lookup_table()

# select all faces within certain radius from center
faces = [f for f in bm.faces if get_distance([0, 0, 0], f.calc_center_median()) < icon_radius]
bmesh.ops.delete(bm, geom=faces, context='FACES')
bm.to_mesh(bpy.context.object.data)

bpy.ops.object.editmode_toggle()

# extrude faces up to qr_height
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, qr_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

# split non-manifold edges
bpy.ops.mesh.select_mode(type="EDGE")
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_non_manifold()
bpy.ops.mesh.edge_split()
bpy.ops.object.editmode_toggle()
bpy.ops.object.editmode_toggle()

if multi:
    bpy.ops.mesh.bevel(offset=0.00025, offset_pct=0, vertex_only=False)

bpy.ops.object.editmode_toggle()

qr = bpy.context.object

# import icon SVG
bpy.ops.import_curve.svg(filepath=icon_path)
objects = bpy.context.scene.objects

# select all curves of SVG and convert to mesh, then join and reset origin
for obj in objects:
    obj.select_set(state = obj.type == "CURVE")
    bpy.context.view_layer.objects.active = obj
    
bpy.ops.object.convert(target='MESH')
bpy.ops.object.join()
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

# resize based on icon_length
icon_scale = icon_length / bpy.context.active_object.dimensions[0]
bpy.context.active_object.scale = (icon_scale, ) * 3

# convert tris to quads
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.tris_convert_to_quads()

# extrude icon up to icon_height
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, icon_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.object.editmode_toggle()

icon = bpy.context.object

# experimental
if multi:
    # join icon and QR
    bpy.ops.object.select_all(action='DESELECT')
    qr.select_set(state = True)
    bpy.context.view_layer.objects.active = qr

    bpy.ops.export_mesh.stl(filepath="interior_no_icon_" + output_path, use_selection=True)
    
    bpy.ops.object.select_all(action='DESELECT')
    icon.select_set(state = True)
    bpy.context.view_layer.objects.active = icon

    bpy.ops.export_mesh.stl(filepath="icon_" + output_path, use_selection=True)

    bpy.ops.object.select_all(action='DESELECT')
    icon.select_set(state = True)
    qr.select_set(state = True)
    bpy.context.view_layer.objects.active = qr

    bpy.ops.object.join()

    bpy.ops.export_mesh.stl(filepath="interior_with_icon_" + output_path, use_selection=True)

    qr = bpy.context.object

    qr = bpy.context.object
    # create base and get it into position    
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.dimensions = (base_length, base_length, 0)
    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, base_height / 2), "orient_type":'NORMAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide() 

    bpy.ops.object.editmode_toggle()

    bpy.context.active_object.location = (0, 0, base_height / 4)

    outside = bpy.context.object 
    modifier = outside.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = qr
    modifier.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    # restore base to rightful place
    outside.location = (0, 0, 0)
    outside.dimensions = (base_length, base_length, base_height)
    outside.scale[2] = 2

    bpy.ops.export_mesh.stl(filepath="exterior_" + output_path, use_selection=True)

else:
    # create and resize base, then extrude down to negative base_height
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.dimensions = (base_length, base_length, 0)
    bpy.ops.object.editmode_toggle()

    bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -base_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    bpy.ops.object.editmode_toggle()
    base = bpy.context.object

    # combine the icon and qr code and base into one object
    qr.select_set(state = True)
    icon.select_set(state = True)

    bpy.ops.object.join()
    
    # export STL to output_path
    bpy.ops.export_mesh.stl(filepath=output_path)
