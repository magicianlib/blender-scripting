bl_info = {
    "name": "Add Subdivided Cube",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "magician lib",
    "description": "Add Subdivided Cube（创建自带细分立方体）",
}

import bpy


def add_subdivided_cube(subdivisions):
    # 创建一个新的立方体
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))

    # 获取新添加的立方体对象
    obj = bpy.context.active_object

    # 进入编辑模式
    bpy.ops.object.mode_set(mode='EDIT')

    # 选择所有的面
    bpy.ops.mesh.select_all(action='SELECT')

    # 细分所有的面
    # 细分面数为1直接退出编辑模式，否者就在细分数基础上减去1
    if subdivisions > 1:
        bpy.ops.mesh.subdivide(number_cuts=subdivisions - 1)

    print(f"subdivide: %s", bpy.ops.mesh.subdivide)

    # 退出编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')

    # 返回新添加的立方体对象
    return obj


def i18n_menu_text():
    """
    i18n:
    Get the menu text based on the current language setting.
    """
    language = bpy.context.preferences.view.language
    if language.startswith('zh_'):
        return "立方体(细分)"
    else:
        return "Add Subdivided Cube"


class OBJECT_OT_add_subdivided_cube(bpy.types.Operator):
    """
    创建自带细分立方体（细分数即为面数）
    """

    bl_idname = "mesh.add_subdivided_cube"
    bl_label = i18n_menu_text()
    bl_options = {'REGISTER', 'UNDO'}

    subdivisions: bpy.props.IntProperty(
        name="Subdivisions",
        description="Number of cuts per face",
        default=2,
        min=1,
        max=100
    )

    def execute(self, context):
        add_subdivided_cube(self.subdivisions)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_add_subdivided_cube.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(OBJECT_OT_add_subdivided_cube)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_subdivided_cube)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
