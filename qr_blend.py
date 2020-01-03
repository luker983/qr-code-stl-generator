import bpy
import bmesh
import os
from math import sqrt

svg_path = 'files/qr.svg'
icon_path = 'files/wifi.svg'
output_path = 'qr.stl'

icon_radius = 0.015

qr_height = 2.5
base_height = 2.5

qr_length = 90
icon_length = 18
base_length = 100

def get_distance(p1,p2):
    distance = sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
    # print(distance)  # print distance to console, DEBUG
    return distance

# delete initial objects

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# import and scale the QR code

bpy.ops.import_curve.svg(filepath=svg_path)

objects = bpy.context.scene.objects

for obj in objects:
    obj.select_set(state = obj.type == "CURVE")
    bpy.context.view_layer.objects.active = obj

bpy.ops.object.convert(target='MESH')
bpy.ops.object.join()
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

bpy.context.active_object.dimensions = (qr_length, qr_length, qr_length)

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.tris_convert_to_quads()

### delete faces
bpy.ops.object.editmode_toggle()

bm = bmesh.new()
bm.from_mesh(bpy.context.object.data)

bm.faces.ensure_lookup_table()

faces = [f for f in bm.faces if get_distance([0, 0, 0], f.calc_center_median()) < icon_radius]
bmesh.ops.delete(bm, geom=faces, context='FACES')
bm.to_mesh(bpy.context.object.data)

bpy.ops.object.editmode_toggle()
### delete faces

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, qr_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.object.editmode_toggle()

qr = bpy.context.object

# create and scale the icon

bpy.ops.import_curve.svg(filepath=icon_path)
objects = bpy.context.scene.objects

for obj in objects:
    obj.select_set(state = obj.type == "CURVE")
    bpy.context.view_layer.objects.active = obj
    
bpy.ops.object.convert(target='MESH')
bpy.ops.object.join()
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

bpy.context.active_object.dimensions = (icon_length, icon_length, icon_length)

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.tris_convert_to_quads()

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 2.5), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.object.editmode_toggle()

icon = bpy.context.object

# create and scale the base

bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 0))
bpy.context.active_object.dimensions = (base_length, base_length, base_length)
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -base_height), "orient_type":'NORMAL', "orient_matrix":((0, 1, -0), (-1, 0, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.object.editmode_toggle()

# combine objects

qr.select_set(state = True)
icon.select_set(state = True)
bpy.ops.object.join()

# export STL

bpy.ops.export_mesh.stl(filepath=output_path)
