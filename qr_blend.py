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
objects = bpy.context.scene.objects
for obj in objects:
    obj.select_set(state = obj.type == "CURVE")
    bpy.context.view_layer.objects.active = obj

# convert curves to mesh
bpy.ops.object.convert(target='MESH')

# join all meshes
bpy.ops.object.join()

# reset object origin (useful for scaling and keeping things centered)
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

# resize based on qr_length
bpy.context.active_object.dimensions = (qr_length, qr_length, qr_length)

# switch to edit mode, select all faces, convert tris to quads
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.tris_convert_to_quads()

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
bpy.context.active_object.dimensions = (icon_length, icon_length, icon_length)

# convert tris to quads
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.tris_convert_to_quads()

# extrude icon up to icon_height
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, icon_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.object.editmode_toggle()

icon = bpy.context.object

# create and resize base, then extrude down to negative base_height
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 0))
bpy.context.active_object.dimensions = (base_length, base_length, base_length)
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -base_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.object.editmode_toggle()

# combine the objects into one
qr.select_set(state = True)
icon.select_set(state = True)
bpy.ops.object.join()

# export STL to output_path
bpy.ops.export_mesh.stl(filepath=output_path)
