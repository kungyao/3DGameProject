bl_info = {
    "name": "3D Game Project",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D Game Project",
    "description": "Add Something",
    "wiki_url": "",
    "category": "Object"}

# if "bpy" in locals():
#     import importlib
#     pass123
# else:
#     pass

import bpy
import bmesh
from random import random
from bpy.types import Panel, PropertyGroup
from bpy.props import BoolProperty, PointerProperty, CollectionProperty

def generatePlane(width, height, density):
    rows = int(height / density)
    columns = int(width / density)
    ary2d = []
    for i in range(rows):
        ary2d.append([])
        for j in range(columns):
            ary2d[i].append((i,j,0))
    return ary2d

class MyCollectionProperty(bpy.types.Operator):
    bl_idname = "line_painter.fill_color_quad"
    bl_label = "Fill Color Quad"
    bl_label = "Fill Color Quad"

    # vertex gap
    density = 1
    width = 10
    height = 10

    def execute(self, context):
        # print(generatePlane(self.width, self.height, self.density))
        mesh = bpy.data.meshes.new("mesh")
        verts = generatePlane(self.width, self.height, self.density)
        bm = bmesh.new()
        for row in verts:
            for column in row:
                bm.verts.new(column)
        bm.to_mesh(mesh)  
        bm.free()
        # mesh.material.append(getDefaultMat())
        obj = bpy.data.objects.new("MyObject", mesh)
        bpy.context.scene.collection.objects.link(obj)  # put the object into the scene (link)
        # bpy.context.scene.objects.active = obj
        
        return {'FINISHED'}

    def modal(self, context, event): 
        print("abc")
        return {'PASS_THROUGH'}

class DesignTool(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_DesignTool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Create"
    bl_label = "設計工具"
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        print("draw")
        layout = self.layout
        row = layout.row()
        row.operator("line_painter.fill_color_quad", text = "刪減地基")

def register():
    bpy.utils.register_class(DesignTool)
    bpy.utils.register_class(MyCollectionProperty)

    # bpy.types.Scene.myProps = CollectionProperty(name="TmpTest", type = MyCollectionProperty)
    # bpy.utils.register_module(MyCollectionProperty)
    print("register")

def unregister():
    # del bpy.types.Scene.myProps
    bpy.utils.unregister_class(DesignTool)
    bpy.utils.unregister_class(MyCollectionProperty)
    print("unregister")

if __name__ == "__main__":
    register()