import bpy
import math
import os
import shutil
class MyProperties(bpy.types.PropertyGroup):
    ani : bpy.props.StringProperty(name = "Animation Name")
    enum : bpy.props.EnumProperty(
        name = "Directions",
        description = "Choose number of directions you want to render.",
        items = [ 
            ("4","4",""),
            ("8","8",""),
            ("16","16","")])

class IsometricRenderPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Isometric Renderer"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        inputs = scene.inputs
        obj = context.object
       
        row = layout.row()
        row.label(text="This guy rendering rendering", icon='WORLD_DATA')
        row = layout.row()
        row.prop(inputs, "entity")
        row = layout.row()
        row.prop(inputs, "ani")
        row = layout.row()
        row.prop(inputs, "enum")
        
        row = layout.row()
        row.operator(IsometricRender.bl_idname)
        row.operator(DeltaRotateZ.bl_idname)
        
class IsometricRender(bpy.types.Operator):
    bl_idname = "render.func_1"
    bl_label = "Render"
    bl_context = "object"

    def execute(self, context):
        
        obj = context.object
        scene = context.scene
        inputs = scene.inputs
        n_directions = int(inputs.enum)
        animation_name = inputs.ani
        angle_inc = 360 / n_directions
        
        path = bpy.data.scenes["Scene"].render.filepath
        os.chdir(path)
        if os.path.isdir(animation_name):
            shutil.rmtree(animation_name)
        os.makedirs(animation_name)
        new_folder_path = path + "/" + animation_name
        os.chdir(new_folder_path)
        if n_directions == 4:     
            direction_list = ["S","E","N","W"]
        elif n_directions  == 8:
            direction_list = ["S","SW","W","NW","N","NE","E","SE"]
            #direction_list = ["S","SE","E","NE","N","NW","W","SW"]
        else:
            direction_list = ["S","SSE","SE","SEE","E","NEE","NE","NNE","N","NNW","NW","NWW","W","SWW","SW","SSW"]
        
        
        for i in range(n_directions):
            bpy.ops.transform.rotate(value= -math.radians(angle_inc), orient_axis = 'Z', center_override=(0,0,0))
            #obj.delta_rotation_euler = [0,0,math.radians(angle)]
            folder = direction_list[i]
            os.makedirs(folder)
            new_render_path = new_folder_path + "/" + folder + "/" + direction_list[i] + "-"
            bpy.data.scenes["Scene"].render.filepath = new_render_path
            bpy.ops.render.render(animation=True, use_viewport = True)
        
        
        bpy.data.scenes["Scene"].render.filepath = path  
        os.chdir(path)
        obj.rotation_euler[1] = 0
        
        return {'FINISHED'}
    
class DeltaRotateZ(bpy.types.Operator):
    bl_idname = "example.func_1"
    bl_label = "Rotate"
    bl_context = "object"
    
    def execute(self, context):
        obj = context.object
        scene = context.scene
        inputs = scene.inputs
        n_directions = int(inputs.enum)
        angle_inc = 360 / n_directions
        bpy.ops.transform.rotate(value=-math.radians(angle_inc), orient_axis = 'Z', center_override=(0,0,0))
        return {'FINISHED'}

classes = [MyProperties, IsometricRender, DeltaRotateZ, IsometricRenderPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.inputs = bpy.props.PointerProperty(type = MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.inputs

if __name__ == "__main__":
    register()
