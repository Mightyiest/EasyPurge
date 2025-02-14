bl_info = {
    "name": "Purge Unused Data",
    "author": "Mightyiest",
    "version": (1, 3),
    "blender": (3, 6, 0),
    "location": "View3D > UI > Purge Unused Data",
    "description": "Remove all unused data-blocks from the project and display purge statistics in the Info Area",
    "category": "Scene",
}

import bpy

def count_data_blocks():
    """Count all data-blocks in the current file."""
    data_blocks = {
        'meshes': len(bpy.data.meshes),
        'materials': len(bpy.data.materials),
        'textures': len(bpy.data.textures),
        'images': len(bpy.data.images),
        'armatures': len(bpy.data.armatures),
        'actions': len(bpy.data.actions),
        'cameras': len(bpy.data.cameras),
        'lights': len(bpy.data.lights),
        'node_groups': len(bpy.data.node_groups),
        'collections': len(bpy.data.collections),
    }
    return data_blocks

class PURGE_OT_unused_data(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.purge_unused_data"
    bl_label = "Purge Unused Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Count data-blocks before purging
        before = count_data_blocks()

        # Detect Blender version and handle accordingly
        if bpy.app.version >= (4, 3, 0):
            # Blender 4.3+ uses a simplified version of the operator
            bpy.ops.outliner.orphans_purge()
        elif bpy.app.version >= (4, 0, 0):
            # Blender 4.0 to 4.2 uses do_local_ids and do_library_ids
            purge_params = {
                'do_local_ids': True,
                'do_library_ids': True
            }
            bpy.ops.outliner.orphans_purge(**purge_params)
        else:
            # Blender 3.6 does not use parameters
            bpy.ops.outliner.orphans_purge()

        # Count data-blocks after purging
        after = count_data_blocks()

        # Calculate the difference
        purged = {key: before[key] - after[key] for key in before}

        # Display the results in the Info Area
        self.report({'INFO'}, 
            f"Purged: "
            f"Meshes: {purged['meshes']}, "
            f"Materials: {purged['materials']}, "
            f"Textures: {purged['textures']}, "
            f"Images: {purged['images']}, "
            f"Armatures: {purged['armatures']}, "
            f"Actions: {purged['actions']}, "
            f"Cameras: {purged['cameras']}, "
            f"Lights: {purged['lights']}, "
            f"Node Groups: {purged['node_groups']}, "
            f"Collections: {purged['collections']}"
        )

        return {'FINISHED'}

# Add a menu entry to access the operator
def menu_func(self, context):
    self.layout.operator("scene.purge_unused_data", text="Purge Unused Data")

def register():
    bpy.utils.register_class(PURGE_OT_unused_data)
    # Add the menu entry
    bpy.types.VIEW3D_MT_editor_menus.append(menu_func)

def unregister():
    bpy.utils.unregister_class(PURGE_OT_unused_data)
    # Remove the menu entry
    bpy.types.VIEW3D_MT_editor_menus.remove(menu_func)

if __name__ == "__main__":
    register()