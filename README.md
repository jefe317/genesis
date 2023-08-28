Infinite Lighting Setups with Ultimate Artistic Control
=======================================================

Genesis is a Blender add-on that helps you make lights in your 3D scene.

Genesis uses artistic color controls to help you make pleasing and unlimited combinations of lighting setups.

6 Color modes, 3 Layout modes, and 5 Light types combined with 8+ customizable settings give you complete control, or the power of stylized chaos with just a click of a button.

Color Modes
-----------

*   Range - Hue value between Min Hue and Max Hue
*   Complementary - 2 Hues from opposite ends of the color wheel - 180 degrees apart
*   Triad - 3 Hues on opposite sides of color wheel - 120 degrees apart
*   Monochromatic - 1 Color, all the same hue
*   Split Complementary - 3 Colors on opposite sides of color wheel - secondary and tertiary colors are +/- 160 degrees apart from the primary color
*   Analogous - 5 Colors on same side of color wheel

Layout Modes
------------

*   Sphere (Creates lights equidistant from the selected object)
*   Top Sphere (Same as Sphere, but creates lights above horizon (+Z))
*   Grid (Creates lights above the selected object in a grid spiraling outward)

Light Types
-----------

*   Point - Emit light in every direction
*   Sun - Emit light from an infinite distance
*   Spot - Emit light in a cone shape
*   Area - Emit light from a plane
*   Plane - Emission shader from a mesh plane

### Changelog

1.0 - Initial Launch


**Getting Started**
===================

Watch on YouTube ([https://www.youtube.com/watch?v=7SzaU47qi1g](https://www.youtube.com/watch?v=7SzaU47qi1g))

1.  Make sure you have downloaded the .zip file onto your computer.
2.  Install and enable the Genesis Add-on by launching Blender and going to **Edit** \> **Preferences** \> **Add-ons** > **Install…** \> Picking the .zip > **Install Add-on**.
3.  With an object selected, Press **N** in the 3D view to show the tool panel if it's hidden, click **Tool**, and expand the **Genesis** panel if it's hidden.
4.  In object mode, select the subject you’d like to add lights to, and click the **Generate Lights** button. That’s it!

**Full Walkthrough**
====================

Watch on YouTube ([https://www.youtube.com/watch?v=GjRN1l3EVsQ](https://www.youtube.com/watch?v=GjRN1l3EVsQ))

Here's everything you need to know about Genesis.

*   Generates GENESIS collection, with child GENESISLights and GENESISUtilities collections
*   **Generate Lights** - Makes collection of lights around the selected object. This will delete any lights or other objects in the GENESISLights folder, so be careful.
*   Light Types:

*   **Point** \- Emit light in every direction
*   **Sun** \- Emit light from an infinite distance
*   **Spot** \- Emit light in a cone shape
*   **Area** \- Emit light from a plane
*   **Plane** \- Emission shader from a mesh plane

*   Color Modes:

*   **Range** \- Hue value between Min Hue and Max Hue
*   **Complementary** \- 2 Hues from opposite ends of the color wheel - 180 degrees apart
*   **Triad** \- 3 Hues on opposite sides of color wheel - 120 degrees apart
*   **Monochromatic** \- 1 Color, all the same hue
*   **Split Complementary** - 3 Colors on opposite sides of color wheel - secondary and tertiary colors are +/- 160 degrees apart from the primary color
*   **Analogous** \- 5 Colors on same side of color wheel

*   Layout Modes:

*   **Sphere** (Creates lights equidistant from the selected object)
*   **Top Sphere** (Same as Sphere, but creates lights above horizon (+Z))
*   **Grid** (Creates lights above the selected object in a grid spiraling outward)

*   **Number** \- How many lights to create (Min 1, Max 200)
*   **Radius** \- How far away the lights are from the selected object in Sphere and Top Sphere Layout mode (Min 0.0001, Max 1000)
*   **Grid Spacing** - How far apart the lights are from each other in Grid Layout mode (Min 0.0001, Max 1000)
*   **Grid Height** - How far up (+Z) the lights are from the selected object in Grid Layout mode (Min 0.0001, Max 1000)
*   **Power Multiplier** - Overall light energy multiplier (Min 0.01, Max 1000)

*   **Min / Max Hue - In Color Range mode, determines what hue values the lights will pick randomly from. 0 and 1 are both red, 0.3 is green, 0.6 is blue. Orange is 0.04, Yellow is 0.17, Teal is 0.5, Purple is 0.7, and Pink is 0.83.**

*   **Base Color** - By clicking the color swatch, you will set the primary color for modes Complementary, Triad, Monochromatic, Split Complementary, and Analogous (not Range)

*   **Hue Spread** - How much randomness in hue to use in color modes Complementary, Triad, Monochromatic, Split Complementary, and Analogous (not Range)

*   **Min / Max Sat** - Multiplier for saturation to use for lights. 1 is full saturation (pure hue colors like red), 0 is no saturation (white).

*   **Min / Max Size** - Size or angle of lights.

*   **Min / Max Power** - Range of randomness for power / wattage / energy for lights.

*   **Lights with Keyframes** - Makes a set of lights per frame in the timeline. Set the range to a small range (1-30 frames) for testing, as it can be slow. It will keyframe the lights on for 1 frame. Useful for testing several lighting setups, or for artistic effects.
*   Note: GENESISEmpty can be moved around to point the lights to a specific spot, or can be deleted to make lights point straight down.
