bl_info = {
    "name": "3D Game Project",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D Game Project",
    "description": "Add Something",
    "wiki_url": "",
    "category": "Object"}

from .Project2.MyParticle import register as particle_register
from .Project2.MyParticle import unregister as particle_unregister

def register():
    print("register")
    particle_register()

def unregister():
    print("unregister")
    particle_unregister()

if __name__ == "__main__":
    register()