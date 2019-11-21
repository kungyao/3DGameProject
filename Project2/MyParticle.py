import bpy

class ParticleItem():
    mass = 1
    gravity = 9.8
    springConnect = []




class ParticlePanel(bpy.types.Panel):
    bl_idname = "UI_PT_ParticlePanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "UI"
    bl_category = "Particle"
    bl_label = "粒子工具"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        select_obj = bpy.context.object

        if "my_particle" in select_obj.keys():
            # draw my particle panel
        
        # draw global setting and another thing
