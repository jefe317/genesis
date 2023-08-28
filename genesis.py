# <pep8 compliant>
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os
import bpy
import bpy.utils.previews
import random
import math
import colorsys

from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )


# ----------------------------------------------------------------------------
#    Functions
# ----------------------------------------------------------------------------


def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found


def save_selected():
    name = bpy.context.view_layer.objects.active.name
    return name


def recall_selected(name):
    if name != '' and name is not None:
        ob = bpy.context.scene.objects[name]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)


def get_offset():
    x = y = z = 0
    if bpy.context.active_object:
        x, y, z = bpy.context.active_object.location
        return x, y, z


def set_position(type="sphere", number=20, radius=5, height=0,
                 offsetx=0, offsety=0, offsetz=0):
    if type == "sphere" or type == "topsphere":
        latDeg = random.randint(0, 360)
        lonDeg = random.randint(0, 360)
        latRad, lonRad = math.radians(latDeg), math.radians(lonDeg)
        x = math.cos(latRad) * math.cos(lonRad) * radius
        y = math.cos(latRad) * math.sin(lonRad) * radius
        if type == "sphere":
            z = math.sin(latRad) * radius
        elif type == "topsphere":
            z = abs(math.sin(latRad) * radius)
        return x + offsetx, y + offsety, z + offsetz
    elif type == "grid":
        z = height
        di = 1
        dj = 0
        seglen = 1
        x = 0
        y = 0
        segpas = 0
        if number == 0:
            return(0 + offsetx, 0 + offsety, z + offsetz)
        for n in range(number):
            x += di
            y += dj
            segpas = segpas + 1
            if n == number - 1:
                return((radius * x) + offsetx,
                       (radius * y) + offsety,
                       z + offsetz)
            if (segpas == seglen):
                segpas = 0
                buffer = di
                di = -dj
                dj = buffer
                if dj == 0:
                    seglen = seglen + 1


def make_tracker(name, collection, parent, x, y, z):
    tracktarget = bpy.context.scene.objects.get(name)
    if tracktarget:
        pass
    else:
        make_collection(collection, parent, True)
        bpy.ops.object.empty_add(type='SPHERE', radius=3, location=(x, y, z))
        bpy.context.active_object.name = name


def track_to(name):
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = bpy.data.objects[name]
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'


def find_collection(name, deselectall=True):
    """not used"""
    if deselectall:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
    col = bpy.data.collections.get(name)
    if col:
        for obj in col.objects:
            obj.select_set(True)


def get_active_collection():
    active_coll = bpy.context.view_layer.active_layer_collection
    # probably want to use the .name of the collection like:
    # active_collection = get_active_collection()
    # set_collection(active_collection.name)
    return active_coll


def select_object(name, deselectall=True):
    """not used"""
    if deselectall:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
    obj = bpy.context.scene.objects.get(name)
    if obj:
        for n in name:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)


def del_all_in_collection(name):
    if bpy.context.blend_data.collections.find(name) > -1:
        delete = bpy.data.collections.get(name)
        for obj in delete.objects:
            bpy.data.objects.remove(obj, do_unlink=True)


def make_collection(name, parent='', active=True):
    # not scene / layer specific, issue, TODO
    if bpy.context.blend_data.collections.find(name) == -1:
        newcoll = bpy.data.collections.new(name)
        if parent:
            parentcoll = bpy.context.scene.collection.children.get(parent)
            parentcoll.children.link(newcoll)
        else:
            bpy.context.scene.collection.children.link(newcoll)
    if active:
        set_collection(name)


def set_collection(name):
    # is scene specific, gets active view layer (scene)
    layer_collection = bpy.context.view_layer.layer_collection
    # print("layer_collection ",layer_collection)
    # print("name ", name)
    layerColl = recurLayerCollection(layer_collection, name)
    # print("layerColl", layerColl)
    bpy.context.view_layer.active_layer_collection = layerColl
    # print("active", bpy.context.view_layer.active_layer_collection)


def make_light(type, color, energy, x, y, z, sizemin='', sizemax='',
               powermin='', powermax=''):
    if type == 'area':
        bpy.ops.object.light_add(type='AREA', radius=1, align='WORLD',
                                 location=(x, y, z))
        bpy.context.object.data.size = random.uniform(sizemin, sizemax)
        bpy.context.object.data.energy = energy * \
            random.uniform(powermin * 10, powermax * 10)
    elif type == 'sun':
        bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD',
                                 location=(x, y, z))
        bpy.context.object.data.angle = \
            random.uniform(sizemin / 2000, sizemax / 2000)
        bpy.context.object.data.energy = energy * \
            random.uniform(powermin / 200, powermax / 200)
    elif type == 'spot':
        bpy.ops.object.light_add(type='SPOT', align='WORLD',
                                 location=(x, y, z))
        bpy.context.object.data.spot_size = \
            random.uniform(sizemin / 10, sizemax / 10)
        bpy.context.object.data.energy = energy * \
            random.uniform(powermin * 400, powermax * 400)
        bpy.context.object.data.spot_blend = 1
    elif type == 'point':
        bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD',
                                 location=(x, y, z))
        bpy.context.object.data.shadow_soft_size = \
            random.uniform(sizemin, sizemax)
        bpy.context.object.data.energy = energy * \
            random.uniform(powermin * 70, powermax * 70)
    if type != 'plane':
        bpy.context.object.data.color = color
    if type == 'plane':
        bpy.ops.mesh.primitive_plane_add(size=random.uniform(sizemin, sizemax),
                                         enter_editmode=False, align='WORLD',
                                         location=(x, y, z))
        # make new material, append to object
        new_mat = bpy.data.materials.new(name="Emit")
        so = bpy.context.active_object
        so.data.materials.append(new_mat)
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes
        material_output = nodes.get("Material Output")
        # set shader to emission
        node_emission = nodes.new(type='ShaderNodeEmission')
        # set emission color
        node_emission.inputs[0].default_value = (color[0],
                                                 color[1],
                                                 color[2], 1)
        # set emission brightness / strength
        node_emission.inputs[1].default_value = energy * \
            random.randint(powermin / 20, powermax / 20)
        # connect the nodes for emission shader
        links = new_mat.node_tree.links
        new_links = links.new(node_emission.outputs[0],
                              material_output.inputs[0])


def set_color(mode, basecolor='', huemin='', huemax='', satmin='',
              satmax='', huespread='', index=''):
    if mode != 'range':
        # convert hue from rgb (blender) to hsv so we can just get the hue
        hsv = colorsys.rgb_to_hsv(basecolor[0], basecolor[1], basecolor[2])
        hue = hsv[0]
        sat = hsv[1]
        # val = hsv[2]
    if mode == 'range':
        # create random hue, saturation for lights, and brightness
        lighthue = random.uniform(huemin, huemax)
        lightsat = random.uniform(satmin, satmax)
        lightval = 1
        lightcolor = colorsys.hsv_to_rgb(lighthue, lightsat, lightval)
    elif mode == 'monochromatic':
        lighthue = hue + (random.uniform(huespread / 100,
                                         - huespread / 100)) + 1
        lightsat = random.uniform(sat * satmin, sat * satmax)
        lightval = random.uniform(0.5, 1.0)
        lightcolor = colorsys.hsv_to_rgb(lighthue, lightsat, lightval)
    elif mode == 'complementary':
        if index % 2 == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 1
        if ((index + 1) % 2) == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 1.5
        lightsat = random.uniform(sat * satmin, sat * satmax)
        lightval = random.uniform(0.7, 1.0)
        lightcolor = colorsys.hsv_to_rgb(lighthue, lightsat, lightval)
    elif mode == 'triad':
        if index % 3 == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 1
        if ((index + 2) % 3) == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 1.33
        if ((index + 1) % 3) == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 0.67
        lightsat = random.uniform(sat * satmin, sat * satmax)
        lightval = random.uniform(0.7, 1.0)
        lightcolor = colorsys.hsv_to_rgb(lighthue, lightsat, lightval)
    elif mode == 'split complementary':
        if index % 3 == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 1
        if ((index + 2) % 3) == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 1.44
        if ((index + 1) % 3) == 0:
            lighthue = hue + (random.uniform(huespread / 100,
                                             -huespread / 100)) + 0.56
        lightsat = random.uniform(sat * satmin, sat * satmax)
        lightval = random.uniform(0.7, 1.0)
        lightcolor = colorsys.hsv_to_rgb(lighthue, lightsat, lightval)
    elif mode == 'analogous':
        if index % 5 == 0:
            lighthue = hue + 1
        if ((index + 4) % 5) == 0:
            lighthue = hue + (random.uniform(huespread / 10,
                                             -huespread / 10)) + 1
        if ((index + 3) % 5) == 0:
            lighthue = hue - (random.uniform(huespread / 10,
                                             -huespread / 10)) + 1
        if ((index + 2) % 5) == 0:
            lighthue = hue + ((random.uniform(huespread / 10,
                                              -huespread / 10)) * 2) + 1
        if ((index + 1) % 5) == 0:
            lighthue = hue - ((random.uniform(huespread / 10,
                                              -huespread / 10)) * 2) + 1
        lightsat = random.uniform(sat * satmin, sat * satmax)
        lightval = random.uniform(0.7, 1.0)
        lightcolor = colorsys.hsv_to_rgb(lighthue, lightsat, lightval)
    return lightcolor


def purge_unused():
    if (2, 83, 0) <= bpy.app.version <= (2, 91, 99):
        bpy.ops.outliner.orphans_purge()
    elif (2, 92, 0) <= bpy.app.version:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_recursive=True)


# ----------------------------------------------------------------------------
#    Scene Properties
# ----------------------------------------------------------------------------

# custom icons for dropdown
preview_collections = {}
# Note that preview collections returned by bpy.utils.previews
# are regular py objects - you can use them to store custom data.
GENESISicons = bpy.utils.previews.new()
# path to the folder where the icon is
# the path is calculated relative to this py file inside the addon folder
# '..' goes up a level, seems to be needed?
# my_icons_dir = os.path.join(os.path.dirname(__file__), '..', "genesis-icons")
my_icons_dir = os.path.join(os.path.dirname(__file__), "genesis-icons")
# load a preview thumbnail of a file and store in the previews collection
GENESISicons.load("icon_mono",
                  os.path.join(my_icons_dir, "monochromatic.png"), 'IMAGE')
GENESISicons.load("icon_comp",
                  os.path.join(my_icons_dir, "complementary.png"), 'IMAGE')
GENESISicons.load("icon_spco",
                  os.path.join(my_icons_dir, "splitcomplementary.png"),
                  'IMAGE')
GENESISicons.load("icon_trid",
                  os.path.join(my_icons_dir, "triad.png"), 'IMAGE')
GENESISicons.load("icon_anlg",
                  os.path.join(my_icons_dir, "analogous.png"), 'IMAGE')
GENESISicons.load("icon_rang",
                  os.path.join(my_icons_dir, "range.png"), 'IMAGE')
preview_collections["main"] = GENESISicons
# create aliases for icon names
customicons = preview_collections["main"]
ic1 = customicons["icon_rang"]
ic2 = customicons["icon_comp"]
ic3 = customicons["icon_trid"]
ic4 = customicons["icon_mono"]
ic5 = customicons["icon_spco"]
ic6 = customicons["icon_anlg"]
# end custom icons for dropdown


class GENESISProperties(PropertyGroup):
    lightmode: EnumProperty(
        name="Light Type:",
        description="Type of light(s) to create",
        items=[('point', "Point Lights", "Emit light in every direction",
                'LIGHT_POINT', 1),
               ('sun', "Sun Lights", "Emit light from an infinite distance",
                'LIGHT_SUN', 2),
               ('spot', "Spot Lights", "Emit light in a cone shape",
                'LIGHT_SPOT', 3),
               ('area', "Area Lights", "Emit light from a plane",
                'LIGHT_AREA', 4),
               ('plane', "Plane Lights", "Emission shader from a plane",
                'MESH_GRID', 5)
               ],
        default='area'
    )

    colormode: EnumProperty(
        name="Color Mode:",
        description="Type of color mode to use for light colors",
        items=[('range', "Range", "Infinite Colors between Min Hue and Max "
                "Hue range on color wheel", ic1.icon_id, 1),
               ('complementary', "Complementary",
                "2 Colors on opposite sides of color wheel", ic2.icon_id, 2),
               ('triad', "Triad", "3 Colors on opposite sides of color wheel",
                ic3.icon_id, 3),
               ('monochromatic', "Monochromatic", "1 Color, all the same hue",
                ic4.icon_id, 4),
               ('split complementary', "Split Complementary",
                "3 Colors on opposite sides of color wheel", ic5.icon_id, 5),
               ('analogous', "Analogous",
                "5 Colors on same side of color wheel", ic6.icon_id, 6)
               ],
        default='range'
    )

    layoutmode: EnumProperty(
        name="Layout Mode:",
        description="How lights should be located in the scene",
        items=[('sphere', "Sphere",
                "Sphere shape layout around the selected object",
                'SPHERE', 1),
               ('topsphere', "Top Sphere",
                "Sphere Shape, but only above the horizon",
                'MATSPHERE', 2),
               ('grid', "Grid",
                "Grid shape layout above the selected object",
                'OUTLINER_DATA_LATTICE', 3)
               ],
        default='sphere'
    )

    lightnumber: IntProperty(
        name="Number",
        description="Total number of lights to create",
        default=9,
        min=1,
        max=200
    )

    lightradius: FloatProperty(
        name="Radius",
        description="Distance between lights and the center point",
        default=40.0,
        min=0.0001,
        max=1000.0
    )

    gridheight: FloatProperty(
        name="Grid Height",
        description="Distance lights are above the horizon",
        default=40.0,
        min=0.0001,
        max=1000.0
    )

    opm: FloatProperty(
        name="Power Multiplier",
        description="Overall light strength",
        default=1.0,
        min=0.01,
        max=1000.0
    )

    basecolor: FloatVectorProperty(
        subtype='COLOR',
        name="Base Color",
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 0.0)
    )

    huemin: FloatProperty(
        name="Min Hue",
        description="Minimum Hue Value (0 red, 0.3 green, 0.6 blue)",
        default=0.0,
        min=0.0,
        max=1.0
    )

    huemax: FloatProperty(
        name="Max Hue",
        description="Maximum Hue Value (0 red, 0.3 green, 0.6 blue)",
        default=1.0,
        min=0.0,
        max=1.0
    )

    huespread: FloatProperty(
        name="Hue Spread",
        description="Hue Range to pick from",
        default=0.1,
        min=0.0,
        max=15.0
    )

    satmin: FloatProperty(
        name="Min Sat",
        description="Minimum Saturation Value (0 no saturation, "
                    "0.5 medium saturation, 1.0 full saturation)",
        default=0.7,
        min=0.0,
        max=1.0
    )

    satmax: FloatProperty(
        name="Max Sat",
        description="Maximum Saturation Value (0 no saturation, "
                    "0.5 medium saturation, 1.0 full saturation)",
        default=1.0,
        min=0.0,
        max=1.0
    )

    sizemin: FloatProperty(
        name="Min Size",
        description="Minimum light size",
        default=7.0,
        min=0.0001,
        max=1000.0
    )

    sizemax: FloatProperty(
        name="Max Size",
        description="Maximum light size",
        default=15.0,
        min=0.0001,
        max=1000.0
    )

    powermin: FloatProperty(
        name="Min Power",
        description="Minimum light strength",
        default=500.0,
        min=0.0,
        max=1000000.0
    )

    powermax: FloatProperty(
        name="Max Power",
        description="Maximum light strength",
        default=1000.0,
        min=0.0,
        max=1000000.0
    )

# ----------------------------------------------------------------------------
#    Operators
# ----------------------------------------------------------------------------


class WM_OT_GENESISGenerateLights(Operator):

    """Add Lights to the Scene"""
    bl_label = "Generate Lights"
    bl_idname = "wm.genesisgenerate"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        lt = scene.genesis_tools

        so = save_selected()
        sox, soy, soz = get_offset()
        active_collection = get_active_collection()
        make_collection("GENESIS")
        del_all_in_collection("GENESISLights")
        purge_unused()
        make_collection("GENESISUtilities", "GENESIS")
        make_tracker("GENESISEmpty", "GENESISUtilities", "GENESIS",
                     sox, soy, soz)
        make_collection("GENESISLights", "GENESIS")
        for l in range(lt.lightnumber):
            x, y, z = set_position(lt.layoutmode, l, lt.lightradius,
                                   lt.gridheight, sox, soy, soz)
            color = set_color(lt.colormode, lt.basecolor,
                              lt.huemin, lt.huemax, lt.satmin, lt.satmax,
                              lt.huespread, l)
            make_light(lt.lightmode, color, lt.opm, x, y, z,
                       lt.sizemin, lt.sizemax, lt.powermin, lt.powermax)
            track_to("GENESISEmpty")
        bpy.ops.object.select_all(action='DESELECT')
        set_collection(active_collection.name)
        recall_selected(so)

        return {'FINISHED'}


class WM_OT_GENESISGenerateLightsWithKeyframes(Operator):

    """Add Lights to the Scene, Keyframed on and off. """ \
        """May take a while to complete if the timeline duration """ \
        """is long. Test with short (less than 10 frame) timelines first"""
    bl_label = "Lights with Keyframes"
    bl_idname = "wm.genesisgeneratekeys"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        lt = scene.genesis_tools
        beg = scene.frame_start
        end = scene.frame_end

        so = save_selected()
        sox, soy, soz = get_offset()
        active_collection = get_active_collection()
        make_collection("GENESIS")
        del_all_in_collection("GENESISLights")
        purge_unused()
        make_collection("GENESISUtilities", "GENESIS")
        make_tracker("GENESISEmpty", "GENESISUtilities", "GENESIS",
                     sox, soy, soz)
        make_collection("GENESISLights", "GENESIS")
        for gindex in range(end):
            for l in range(lt.lightnumber):
                x, y, z = set_position(lt.layoutmode, l, lt.lightradius,
                                       lt.gridheight, sox, soy, soz)
                color = set_color(lt.colormode, lt.basecolor,
                                  lt.huemin, lt.huemax, lt.satmin, lt.satmax,
                                  lt.huespread, l)
                make_light(lt.lightmode, color, lt.opm, x, y, z,
                           lt.sizemin, lt.sizemax, lt.powermin, lt.powermax)
                track_to("GENESISEmpty")
                obj = bpy.context.object
                frame = gindex + 1
                previousframe = frame - 1
                nextframe = frame + 1
                obj.hide_render = True
                obj.hide_viewport = True
                obj.keyframe_insert(data_path="hide_render",
                                    frame=previousframe)
                obj.keyframe_insert(data_path="hide_viewport",
                                    frame=previousframe)
                obj.hide_render = False
                obj.hide_viewport = False
                obj.keyframe_insert(data_path="hide_render",
                                    frame=frame)
                obj.keyframe_insert(data_path="hide_viewport",
                                    frame=frame)
                obj.hide_render = True
                obj.hide_viewport = True
                obj.keyframe_insert(data_path="hide_render",
                                    frame=nextframe)
                obj.keyframe_insert(data_path="hide_viewport",
                                    frame=nextframe)
        bpy.ops.object.select_all(action='DESELECT')
        set_collection(active_collection.name)
        recall_selected(so)

        return {'FINISHED'}


# ----------------------------------------------------------------------------
#    Panel in Object Mode
# ----------------------------------------------------------------------------


class OBJECT_PT_CustomPanel(Panel):

    """Generates light creation tools in 3D viewport Sidebar [N]"""
    bl_label = "Genesis"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        global custom_icons
        layout = self.layout
        scene = context.scene
        genesistools = scene.genesis_tools
        # duration = scene.frame_end - scene.frame_start

        col = layout.column(align=True)
        # generate lights button
        col.operator("wm.genesisgenerate", icon='LIGHT')
        col.separator()
        # light/color type dropdown
        col.prop(genesistools, "lightmode", text="Type")
        col.prop(genesistools, "colormode", text="Colors")
        col.prop(genesistools, "layoutmode", text="Layout")
        col.prop(genesistools, "lightnumber")
        if genesistools.layoutmode == 'grid':
            col.prop(genesistools, "lightradius", text="Grid Spacing")
            col.prop(genesistools, "gridheight")
        else:
            col.prop(genesistools, "lightradius")
        col.prop(genesistools, "opm")
        if genesistools.colormode == 'range':
            col.label(text="Hue:")
            col.prop(genesistools, "huemin")
            col.prop(genesistools, "huemax")
        else:
            col.prop(genesistools, "basecolor")
            col.prop(genesistools, "huespread")
        col.label(text="Saturation:")
        col.prop(genesistools, "satmin")
        col.prop(genesistools, "satmax")
        if genesistools.lightmode == 'spot':
            col.label(text="Spot Size / Angle:")
        else:
            col.label(text="Size:")
        col.prop(genesistools, "sizemin")
        col.prop(genesistools, "sizemax")
        col.label(text="Power:")
        col.prop(genesistools, "powermin")
        col.prop(genesistools, "powermax")
        col.separator()
        col.operator("wm.genesisgeneratekeys", icon='RENDER_ANIMATION')


# ----------------------------------------------------------------------------
#    Registration
# ----------------------------------------------------------------------------

classes = (
    GENESISProperties,
    WM_OT_GENESISGenerateLights,
    WM_OT_GENESISGenerateLightsWithKeyframes,
    OBJECT_PT_CustomPanel
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.genesis_tools = PointerProperty(type=GENESISProperties)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.genesis_tools
    # remove custom icons
    for GENESISicons in preview_collections.values():
        bpy.utils.previews.remove(GENESISicons)
    preview_collections.clear()


if __name__ == "__main__":
    # The path of this text (if saved)
    __file__ = bpy.context.space_data.text.filepath
    register()
