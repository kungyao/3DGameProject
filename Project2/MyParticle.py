import bpy
import bmesh
from mathutils import Vector
from bpy.props import IntProperty, FloatProperty, EnumProperty, StringProperty, CollectionProperty, BoolProperty

class SpringConnect(bpy.types.PropertyGroup):
    name : StringProperty(name="Object Name", default="")

class ParticlePoperty(bpy.types.PropertyGroup):
    name            : StringProperty(name = "Object Name", default = "")
    play            : BoolProperty(name = "Play", default = False)
    kinematic       : BoolProperty(name = "Kinematics", default = False)
    mass            : IntProperty(name = "Mass", default = 1, min = 0)
    velocity_x      : FloatProperty(name = "Velocity_x", default = 0)
    velocity_y      : FloatProperty(name = "Velocity_y", default = 0)
    velocity_z      : FloatProperty(name = "Velocity_z", default = 0)
    force_x         : FloatProperty(name = "Force_x", default = 0)
    force_y         : FloatProperty(name = "Force_y", default = 0)
    force_z         : FloatProperty(name = "Force_z", default = 0)
    gravity         : FloatProperty(name = "Gravity", default = -9.8)
    springConnects  : CollectionProperty(name = "Spring Connects", type = SpringConnect)

class ParticleAdd(bpy.types.Operator):
    bl_idname = "particle_ops.add_particle"
    bl_label = "Add Particle"

    CircleSegmentCount = 64
    CircleVertexCount = CircleSegmentCount + 2
    CircleIndexCount = CircleSegmentCount * 3

    def execute(self, context):
        print("Add")
        scene = context.scene
        
        mesh = bpy.data.meshes.new('TEST_MESH')
        obj =  bpy.data.objects.new("TEST_OBJ", mesh)

        if scene.createParticleType == "CIRCLE":
            print("CIRCLE")
        elif scene.createParticleType == "PLANE":
            print("PLANE")
        elif scene.createParticleType == "TEST":
            print("TEST")

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.to_mesh(mesh)
        bm.free()
        
        obj['p_flag'] = True
        prop = scene.myParticleList.add()
        prop.name = obj.name
        scene.collection.objects.link(obj)
        return {"FINISHED"}

class ParticleDelete(bpy.types.Operator):
    bl_idname = "particle_ops.delete_particle"
    bl_label = "Delete Particle"

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj == None:
            return False
        return 'p_flag' in obj.keys()

    def execute(self, context):
        print("Delete")
        obj = context.object
        itemIndex = context.scene.myParticleList.find(obj.name)
        # remove from property list
        context.scene.myParticleList.remove(itemIndex)
        # remove from world
        bpy.data.objects.remove(obj)
        return {"FINISHED"}

class ParticlePanel(bpy.types.Panel):
    bl_idname = "UI_PT_ParticlePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Particle"
    bl_label = "粒子工具"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        select_obj = context.object
        scene = context.scene
        layout = self.layout

        # draw global setting and another thing
        layout.prop(scene, 'createParticleType')

        box = layout.box()
        box.operator("particle_ops.add_particle")
        box.operator("particle_ops.delete_particle")

        if select_obj != None and 'p_flag' in select_obj.keys():
            item = scene.myParticleList.get(select_obj.name)
            if item != None:
                layout.label(text = item.name)
                # layout.prop(item, 'name')
                layout.prop(item, 'play')
                layout.prop(item, 'kinematic')
                layout.prop(item, 'mass')
                # layout.prop(item, 'velocity_x')
                # layout.prop(item, 'velocity_y')
                # layout.prop(item, 'velocity_z')
                layout.prop(item, 'gravity')
            pass

def EulerIntegration(pos, mass, velocity, gravity, force):
    scene = bpy.context.scene
    newVelocity = velocity + scene.frameRate * (mass * Vector((0, 0, gravity)) + force)
    newPos = pos + scene.frameRate * newVelocity
    return newPos, newVelocity

def AddForce(obj, p_prop):
    vVec = Vector((p_prop.velocity_x, p_prop.velocity_y, p_prop.velocity_z))
    # aVec = Vector((p_prop.acceration_x, p_prop.acceration_y, p_prop.acceration_z))
    mass = p_prop.mass
    gravity = p_prop.gravity
    # calcluate new info
    obj.location, vVec = EulerIntegration(obj.location, mass, vVec, gravity)
    # give porperty back
    p_prop.velocity_x, p_prop.velocity_y, p_prop.velocity_z = vVec
    # p_prop.acceration_x, p_prop.acceration_y, p_prop.acceration_z = aVec

def ResetVelocity(p_prop):
    # reset velocity
    p_prop.velocity_x = 0
    p_prop.velocity_y = 0
    p_prop.velocity_z = 0

def ResetForce(p_prop):
    p_prop.force_x = 0
    p_prop.force_y = 0
    p_prop.force_z = 0

def Update():
    scene = bpy.context.scene
    # 初始化外力
    for par in scene.myParticleList:
        ResetForce(par)
    for par in scene.myParticleList:
        if par.play:
            if par.kinematic:
                ResetVelocity(par)
                continue
            obj = bpy.data.objects.get(par.name)
            AddForce(obj, par)
    # for par in scene.myParticleList:
    return scene.frameRate

def register():
    print("p_register")
    # register class
    bpy.utils.register_class(ParticlePanel)
    bpy.utils.register_class(ParticleAdd)
    bpy.utils.register_class(ParticleDelete)
    bpy.utils.register_class(SpringConnect)
    bpy.utils.register_class(ParticlePoperty)
    # create global variable
    bpy.types.Scene.frameRate = 0.02
    bpy.types.Scene.createParticleType = EnumProperty(
        items = [("CIRCLE", "Circle", ""), ("PLANE", "Plane", ""), ("CUBE", "Cube", "")],
        name = "Particle Type"
    )
    bpy.types.Scene.myParticleList = CollectionProperty(name = "Particles", type = ParticlePoperty)
    # bpy.types.Scene.myParticleObjList = []
    # register my update function
    bpy.app.timers.register(Update, first_interval = 0.02)

def unregister():
    print("p_unregister")
    # unregister class
    bpy.utils.unregister_class(ParticlePanel)
    bpy.utils.unregister_class(ParticleAdd)
    bpy.utils.unregister_class(ParticleDelete)
    bpy.utils.unregister_class(SpringConnect)
    bpy.utils.unregister_class(ParticlePoperty)
    # delete global variable
    del bpy.types.Scene.frameRate
    del bpy.types.Scene.createParticleType
    del bpy.types.Scene.myParticleList
    # del bpy.types.Scene.myParticleObjList
    # unregister my update function
    bpy.app.timers.unregister(Update)
