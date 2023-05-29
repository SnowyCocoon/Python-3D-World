import bpy
from math import radians
from bpy.props import *

class MyOperator(bpy.types.Operator):
    bl_idname = "object.my_operator"
    bl_label = "My Operator"
    bl_options = {'REGISTER', 'UNDO'}
    
    #create properties
    noise_scale : FloatProperty(
        name = "Noise Scale",
        description = "The scale of the noise",
        default = 1.0,
        min = 0.0,
        max = 3.0
    )
    

    def execute(self, context):
        
        bpy.ops.mesh.primitive_cube_add()
        so = bpy.context.active_object
            
        #move object
        so.location[0] = 0

        #rotate object
        so.rotation_euler[0] += radians(45)

        #create modifier
        mod_subsurf = so.modifiers.new("My Modifier", 'SUBSURF')

        #change modifier value
        so.modifiers["My Modifier"].levels =3
        #or
        mod_subsurf.levels = 3

        #smoothing the mesh
        #bpy.ops.object.shade_smooth()
        mesh = so.data
        for face in mesh.polygons:
            face.use_smooth = True

        #Create displacement modifier
        mod_displace = so.modifiers.new("My Displacement", 'DISPLACE')

        #create the texture
        new_tex = bpy.data.textures.new("My Texture", 'DISTORTED_NOISE')

        #change the texture settings
        new_tex.noise_scale = self.noise_scale

        #assign the texture to displacement modifier
        mod_displace.texture = new_tex

        #create the material
        new_mat = bpy.data.materials.new(name = "My Material")
        so.data.materials.append(new_mat)

        #Turn on the nodes
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes

        #Create output node
        material_output = nodes.get("Material Output")

        #Create and set the emission node
        node_emission = nodes.new(type='ShaderNodeEmission')
        node_emission.inputs[0].default_value = (0.0, 0.3, 1.0, 1) #color
        node_emission.inputs[1].default_value = 500.0 #strength

        #link the nodes on material graph
        links = new_mat.node_tree.links
        new_link = links.new(node_emission.outputs[0], material_output.inputs[0])
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MyOperator)


def unregister():
    bpy.utils.unregister_class(MyOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.my_operator()
