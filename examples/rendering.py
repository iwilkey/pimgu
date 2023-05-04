###################################################################################
# A simple framework for creating robust 2D GUI applications using Pygame and ImGui
# Author: Ian Wilkey (iwilkey)
# Copyright (C) 2023 Ian Wilkey. All Rights Reserved.
# License: MIT.
# Version: v05.04.2023
###################################################################################

# To be explicit about what type that Pimgu expects your Pygame render callbacks to be.
from typing import Tuple
# or direct use of all the beautiful functions of Pygame.
import pygame
# For direct use of all the beautiful functions of Dear ImGui.
import imgui
# The only Pimgu class you have to worry about :).
from pimgu import Applet

def pygame_surface_render_callback() -> Tuple[pygame.Surface, int, int]:
    """ Example Pygame render callback that draws a red square.

    Returns:
        Tuple[pygame.Surface, int, int]: Every Pygame render callback MUST return the surface you created
            and the center x and center y to draw the surface on.
    """
    # Surface defined as 100 x 100.
    surface = pygame.Surface((100, 100))
    # Surface will be rendered with its center at the point defined below.
    center_x, center_y = 200, 150
    
    # NOTE: All Pygame methods that relate to surfaces apply here. Be creative!
    
    # Draw a red filled rectangle on the surface, the same size as the surface.
    pygame.draw.rect(surface, (255, 0, 0), (0, 0, 100, 100))
    
    # Remember to return the parameters in this order, or else nasty things will occur!
    return surface, center_x, center_y

def pygame_surface_render_callback2() -> Tuple[pygame.Surface, int, int]:
    """ Example Pygame render callback that draws a green square.

    Returns:
        Tuple[pygame.Surface, int, int]: Every Pygame render callback MUST return the surface you created
            and the center x and center y to draw the surface on.
    """
    # Surface defined as 100 x 100.
    surface = pygame.Surface((100, 100))
    # Surface will be rendered with its center at the point defined below.
    center_x, center_y = 500, 277
    
    # NOTE: All Pygame methods that relate to surfaces apply here. Be creative!
    
    # Draw a green filled rectangle on the surface, the same size as the surface.
    pygame.draw.rect(surface, (0, 255, 0), (0, 0, 100, 100))
    
    # Remember to return the parameters in this order, or else nasty things will occur!
    return surface, center_x, center_y

def pimgu_gui_window():
    """ This defines a "GUI callback", which is called during a Pimgu Applet's ImGui render time.
    Feel free to use any imgui.*() functions here to build your GUI. In this case, we are creating
    a simple window that reads "Hello, world!".
    """
    # Creating a simple window.
    imgui.begin("My First Pimgu Window!")
    # Adding text to it.
    imgui.text("Hello, world!")
    
    # NOTE: All the Dear Imgui Python bindings functions can be called here, so be creative!

    # Ending this windows ImGui calls. (Important!)
    imgui.end()

# Example of setting the frame rate.
app = Applet()

# Example of setting the frame rate. In this case, we are setting the target frame rate of the
# application to 59 frames per second.
app.set_target_fps(59.0)

# Always remember to register your callbacks! Make sure you specify the right one, or else nasty
# things can happen during runtime.
app.register_pygame_render_callback(pygame_surface_render_callback)
app.register_pygame_render_callback(pygame_surface_render_callback2)
app.register_imgui_callback(pimgu_gui_window)

# Run the Pimgu application after you have registered all of your callbacks. Keep in mind, this will
# block the main thread, so no code under this will be called until the Pimgu application stops running.
# NOTE: If you'd like to do parallel processes, it is recommended to use Pythons "threading" package.
# Just be sure to always run Pimgu in the main thread.
app.run()
