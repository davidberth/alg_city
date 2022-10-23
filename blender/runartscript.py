bl_info = {
    "name": "Run Art Script",
    "blender": (3, 0, 0),
    "category": "Scene",
    "author": "David Berthiaume",
    "description": "This addon runs an external script.",
    "location": "View3D > Add > Mesh",
    "version": (1, 0)
    }
    
     

import bpy
import os
import sys
import importlib

addon_keymaps = []

class RunArtScript(bpy.types.Operator):
    """Runs an external script in ../alg_city/blender.py"""
    bl_idname = "object.runscript"
    bl_label = "Run external script"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
    
        script_path = os.path.join(os.path.dirname(bpy.data.filepath), '../alg_city')
        print (f'running the external script at {script_path}/blender.py !')
                        
        if script_path not in sys.path:
            sys.path.append(script_path)
        import blender
        importlib.reload(blender)
        blender.blender()

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(RunArtScript.bl_idname)
    
def register():
    bpy.utils.register_class(RunArtScript)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(RunArtScript.bl_idname, 'F5', 'PRESS', ctrl=False, shift=False)
        addon_keymaps.append((km, kmi))
    
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(RunArtScript)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()

