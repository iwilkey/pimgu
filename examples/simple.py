###################################################################################
# A simple framework for creating robust 2D GUI applications using Pygame and ImGui
# Author: Ian Wilkey (iwilkey)
# Copyright (C) 2023 Ian Wilkey. All Rights Reserved.
# License: MIT.
# Version: v05.04.2023
###################################################################################

# For direct use of all the beautiful functions of ImGui.
import imgui
# The only Pimgu class you have to worry about :).
from pimgu import Applet

def pimgu_gui_window():
    """ This defines a "GUI callback", which is called during a Pimgu Applet's ImGui render time.
    Feel free to use any imgui.*() functions here to build your GUI. In this case, we are creating
    a simple window that reads "Hello, world!".
    """
    imgui.begin("My First Pimgu Window!")
    imgui.text("Hello, world!")
    imgui.end()

# Create the Pimgu applet.
app = Applet(title="Pimgu Example")

# Example of setting the frame rate. In this case, we are setting the target frame rate of the
# application to 59 frames per second.
app.set_target_fps(59.0)

# Always remember to register your callbacks! Make sure you specify the right one, or else nasty
# things can happen during runtime.
app.register_imgui_callback(pimgu_gui_window)

# Run the Pimgu application after you have registered all of your call backs. Keep in mind, this will
# block the main thread, so no code under this will be called until the Pimgu application stops running.
# NOTE: If you'd like to do parallel processes, it is recommended to use Pythons "threading" package.
# Just be sure to always run Pimgu in the main thread.
app.run()
