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

import bpy
from . import genesis

# CHANGELOG
# v 0.0.1 February 2022 - Genesis - Light Generator
#   ☒ Initial Add-on with light types, color modes, and layout control
#   ☒ Light Types:
#       ☒ Point
#       ☒ Sun
#       ☒ Spot
#       ☒ Area
#       ☒ Plane
#   ☒ Color Modes:
#       ☒ Range (Hue value between Min Hue and Max Hue)
#       ☒ Complementary (2 Hues from opposite ends of the color wheel)
#       ☒ Triad (3 Hues on opposite sides of color wheel)
#       ☒ Monochromatic (1 Color, all the same hue)
#       ☒ Split Complementary (3 Colors on opposite sides of color wheel)
#       ☒ Analogous (5 Colors on same side of color wheel)
#   ☒ Layout Modes:
#       ☒ Sphere (Creates lights equidistant from the selected object)
#       ☒ Top Sphere (Same as Sphere, but creates lights above horizon (+Z))
#       ☒ Grid (Creates lights above the selected object in a grid
#         spiraling outward)
#   ☒ Generates GENESIS collection, with child GENESISLights and
#     GENESISUtilities collections.
#   ☒ Lights with Keyframes:
#       ☒ Makes a set of lights per frame in the timeline. Set the range to
#         a small range (3-10 frames) for testing, as it can be slow. It will
#         keyframe the lights on for 1 frame. Useful for testing several
#         lighting setups, or for artistic effects.

bl_info = {
    "name": "Genesis - Light Generator",
    "description": "Tools to create lights in a 3D scene",
    "author": "Jeff Lange - @jefftml",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar > Tool",
    "doc_url": "https://jefftml.com/genesis-docs",
    "wiki_url": "https://jefftml.com/genesis-docs",
    "category": "Lighting"
}
# todo: IES/lighting gobos/patterns via duplication
#       predefined lighting setups
#       vertical circles layout, box layout,
#       update existing lights with settings without deletion
# bugs: issues with multiple scenes if collection exists in non-active scene


def register():
    genesis.register()


def unregister():
    genesis.unregister()


if __name__ == "__main__":
    register()
