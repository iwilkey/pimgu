###################################################################################
# A simple framework for creating robust 2D GUI applications using Pygame and ImGui
# Author: Ian Wilkey (iwilkey)
# Copyright (C) 2023 Ian Wilkey. All Rights Reserved.
# License: MIT.
# Version: v05.04.2023
###################################################################################

# Python standards.
import os
from typing import List, Callable, Tuple
# Dependencies.
import pygame as engine
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import imgui
from imgui.integrations.pygame import PygameRenderer

version = "v05.04.2023.6"

#################################################
# OpenGL Helper Methods to make our lives easier.
#################################################

def pygame_surface_to_opengl_texture(surface) -> int:
    """ Helper method that accepts a Pygame Surface object and converts it to an
    OpenGL texture that can be rendered by the Pimgu renderer.
    Args:
        surface (pygame.Surface): The surface to be rendered.
    Returns:
        texture_id: The OpenGL texture ID to be rendered.
    """
    width, height = surface.get_size()
    texture_data = engine.image.tostring(surface, "RGBA", 1)
    texture_id : int = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return texture_id

def draw_texture(texture_id : int, surface_width : int, surface_height : int, center_x : int, center_y : int):
    """ Helper method that accepts a texture ID and renders it to the screen with
    a given width and height at the given center point.
    Args:
        texture_id: The OpenGL texture ID.
        surface_width (int): The width of the rendered surface.
        surface_height (int): The height of the rendered surface.
        center_x (int): The center X location of the rendered surface.
        center_y (int): The center Y location of the rendered surface.
    """
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Compute the quad vertices.
    x1, y1 = center_x, center_y
    x2, y2 = center_x + surface_width, center_y
    x3, y3 = center_x + surface_width, center_y + surface_height
    x4, y4 = center_x, center_y + surface_height

    # Draw the quad with the texture.
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x1, y1, 0)
    glTexCoord2f(1, 0); glVertex3f(x2, y2, 0)
    glTexCoord2f(1, 1); glVertex3f(x3, y3, 0)
    glTexCoord2f(0, 1); glVertex3f(x4, y4, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    
    # Delete the texture after rendering. This will prevent a memory leak.
    # NOTE: This isn't the most efficient thing to do, but it doesn't matter as mucn since this
    # application framework is not meant for high performance rendering, just GUI applications.
    glDeleteTextures(1, [texture_id])

#####################
# Pimgu Applet class.
#####################

class Applet:
    """ Core framework for a Pimgu Applet. Supports robust, high-level tools for powerful 2D GUI applications.
    """
    
    def __init__(self, title : str = "Pimgu Application", dimensions : tuple = (1280, 720), icon_path : str = "", **kwargs):
        """ Construct a new Pimgu Applet.\n
        Args:
            title (string): The title of the application.\n
            dimensions (tuple): The dimensions of the window (width, height).\n
            icon_path (string): Path to the window icon (optional).
        """
        
        # Initialize Pygame (core engine).
        engine.init()
        
        # Set the target FPS.
        self.__target_fps : int = 60
        
        ##################
        # Window Context #
        ##################
        
        # Window metadata.
        self.__title : str = title
        self.__dimensions : tuple = dimensions
        self.__icon_path : str = icon_path
        # Set the windows title.
        engine.display.set_caption(self.__title)
        # Set the windows icon, if supplied.
        if self.__icon_path != "":
            # Check if icon path exists.
            if not os.path.exists(self.__icon_path):
                raise Exception("[PIMGU] Invalid icon path!")
            # Load the icon image.
            icon = engine.image.load(self.__icon_path)
            # Set the icon of the window.
            engine.display.set_icon(icon)
        
        # Set up the screen.
        self.__screen : engine.Surface = engine.display.set_mode(self.__dimensions, engine.OPENGL | engine.DOUBLEBUF)

        # Set up OpenGL context.
        glViewport(0, 0, self.__dimensions[0], self.__dimensions[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.__dimensions[0], self.__dimensions[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Clear color.
        self.__cls_color : tuple = (0.1, 0.1, 0.1, 1)

        # Get clock object.
        self.__clock : engine.time.Clock = engine.time.Clock()

        #################
        # ImGui Context #
        #################
        
        # Create the ImGui context.
        imgui.create_context()
        # Retrieve the ImGui IO buffer.
        self.__imgui_io = imgui.get_io()
        # ImGui IO configuration.
        self.__imgui_io.display_size = self.__screen.get_width(), self.__screen.get_height()
        self.__imgui_io.delta_time = 1.0 / self.__target_fps
        self.__imgui_io.backend_flags |= imgui.BACKEND_HAS_MOUSE_CURSORS
        # Set up ImGui renderer.
        self.__imgui_renderer : PygameRenderer = PygameRenderer()
        
        #############
        # CALLBACKS #
        #############

        # Callbacks during input processing stage.
        self.__input_callbacks : List[Callable] = []
        # Callbacks during GUI processing state.
        self.__imgui_callbacks : List[Callable] = []
        # Callbacks during render time (for Pygame).
        self.__render_callbacks : List[Callable[..., Tuple[engine.Surface, int, int]]] = []
        # Callbacks during tick time (before any rendering).
        self.__tick_callbacks : List[Callable] = []
        # Called when the Pimgu application is closed.
        self.__on_end_callback : Callable = None
        
        # Run the application.
        self.__running : bool = False
        
    def run(self):
        """ Runs the main loop of the application.
        """
        self.__running = True

        while self.__running:
            # Sync the engine to frame rate.
            self.__sync()
            # Receive and process input events.
            self.__process_events()
            # Handle ImGui calls.
            self.__handle_gui()
            # Custom tick callbacks.
            for callback in self.__tick_callbacks:
                callback()
            # Clear the screen.
            self.__cls()
            # Render.
            self.__render()
            
        self.__on_end_callback()
        self.__imgui_renderer.shutdown()
        engine.quit()
        
    def __sync(self):
        """ Sync the engine to the target frame rate.
        """
        self.__clock.tick(self.__target_fps)
        
    def __process_events(self):
        """ Handle input for Pygame and ImGui.
        """
        events = engine.event.get()
        for event in events:
            if event.type == engine.QUIT:
                self.set_running(False)
            else:
                self.__imgui_renderer.process_event(event)
            # Call custom input callbacks.
            for callback in self.__input_callbacks:
                callback(event = event)

    def __handle_gui(self):
        """ Handle custom ImGui calls and frame context.
        """
        imgui.new_frame()
        # Call custom ImGui callbacks.
        for callback in self.__imgui_callbacks:
            callback()
        imgui.end_frame()
        
    def __cls(self):
        """ Clear the GL color buffer.
        """
        glClearColor(self.__cls_color[0], self.__cls_color[1], self.__cls_color[2], self.__cls_color[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def __render(self):
        """ Render the current state of the applet.
        """
        
        # Custom Pygame Surface render callbacks.
        for callback in self.__render_callbacks:
            try:
                surface, cx, cy = callback()
            except TypeError:
                raise Exception("[PIMGU] When it is desired to draw a pygame surface to the screen, your callback must return: surface, center_x, center_y! See Pimgu examples on GitHub: https://github.com/iwilkey/pimgu.")
            # Surface dimensions.
            width, height = surface.get_size()
            texture_id : int = pygame_surface_to_opengl_texture(surface)
            draw_texture(texture_id, width, height, cx, cy)
        
        # Draw ImGui data to renderer.
        imgui.render()
        self.__imgui_renderer.render(imgui.get_draw_data())
        
        # Flip the display color buffers to render.
        engine.display.flip()
        
    #############
    # REGISTERS #
    #############
            
    def register_input_callback(self, callback : Callable):
        """ Register a callback to be called during Applet input processing.
        """
        self.__input_callbacks.append(callback)
        
    def register_imgui_callback(self, callback : Callable):
        """ Register a callback to be called during Applet GUI processing.
        """
        self.__imgui_callbacks.append(callback)

    def register_pygame_render_callback(self, callback : Callable[..., Tuple[engine.Surface, int, int]]):
        """ Register a callback to be called during Pygame render time.
        """
        self.__render_callbacks.append(callback)
        
    def register_tick_callback(self, callback : Callable):
        """ Regsiter a callback to be called during the Applet's tick stage (before rendering, after input.)
        """
        self.__tick_callbacks.append(callback)
    def register_on_end_callback(self, callback : Callable):
        """ Register a callback to occur when the application is terminated (running = False after running).
        """
        self.__on_end_callback = callback
    
    #######################
    # GETTERS AND SETTERS #
    #######################
    
    def get_title(self) -> str:
        return self.__title
    
    def get_screen(self) -> engine.Surface:
        return self.__screen

    def get_imgui_io(self):
        return self.__imgui_io

    def get_imgui_renderer(self) -> PygameRenderer:
        return self.__imgui_renderer
    
    def get_clock(self) -> engine.time.Clock:
        return self.__clock
    
    def get_cls_color(self) -> tuple:
        return self.__cls_color
    
    def is_running(self) -> bool:
        return self.__running
    
    def get_target_fps(self) -> int:
        return self.__target_fps
    
    def set_cls_color(self, cls_color : tuple):
        self.__cls_color = cls_color
        
    def set_running(self, running : bool):
        self.__running = running

    def set_target_fps(self, target_fps : int):
        self.__target_fps = target_fps
