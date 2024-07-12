bl_info = {
    "name": "Show Object Axes",
    "blender": (3, 3, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "magician lib",
    "description": "Show or hide axes for all objects and new objects（显示或隐藏所有对象和新对象的坐标轴）",
}

import bpy

# Global variable to keep track of axes display state
axes_shown = False


def set_show_axis(obj, show=True):
    """Enable or disable axis display for the given object."""
    if hasattr(obj, "show_axis"):
        obj.show_axis = show


def show_axes_for_all_objects(show=True):
    """Enable or disable axis display for all existing objects."""
    for obj in bpy.context.scene.objects:
        set_show_axis(obj, show)


def on_object_add(scene, depsgraph):
    """Handler to enable or disable axis display for new objects."""
    for update in depsgraph.updates:
        if isinstance(update.id, bpy.types.Object):
            set_show_axis(update.id, axes_shown)


class ToggleObjectAxes(bpy.types.Operator):
    """Toggle axes display for all objects and new objects"""
    bl_idname = "object.toggle_axes"
    bl_label = "Toggle Axes Display"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global axes_shown
        axes_shown = not axes_shown
        show_axes_for_all_objects(axes_shown)
        if axes_shown:
            if on_object_add not in bpy.app.handlers.depsgraph_update_post:
                bpy.app.handlers.depsgraph_update_post.append(on_object_add)
            self.report({'INFO'}, "Axes display enabled for all objects and new objects.")
        else:
            if on_object_add in bpy.app.handlers.depsgraph_update_post:
                bpy.app.handlers.depsgraph_update_post.remove(on_object_add)
            self.report({'INFO'}, "Axes display disabled for all objects.")
        # Force UI update
        bpy.context.area.tag_redraw()
        return {'FINISHED'}


def i18n_menu_text():
    """
    i18n:
    Get the menu text based on the current language setting.
    """
    language = bpy.context.preferences.view.language
    if language.startswith('zh_'):
        return "隐藏物体轴向", "显示物体轴向"
    else:
        return "Hide Axes Display", "Show Axes Display"


def draw_toggle_axes_menu(self, context):
    global axes_shown
    hide_text, show_text = i18n_menu_text()
    if axes_shown:
        self.layout.operator(ToggleObjectAxes.bl_idname, text=hide_text)
    else:
        self.layout.operator(ToggleObjectAxes.bl_idname, text=show_text)


def register():
    bpy.utils.register_class(ToggleObjectAxes)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_toggle_axes_menu)


def unregister():
    bpy.utils.unregister_class(ToggleObjectAxes)
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_toggle_axes_menu)
    if on_object_add in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(on_object_add)


if __name__ == "__main__":
    register()
