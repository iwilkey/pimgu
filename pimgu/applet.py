###################################################################################
# A simple framework for creating robust 2D GUI applications using Pygame and ImGui
# Author: Ian Wilkey (iwilkey)
# Copyright (C) 2023 Ian Wilkey. All Rights Reserved.
# License: MIT.
# Version: v05.04.2023
###################################################################################

# Python standards.
import sys
import os
from typing import List, Callable
# Dependencies.
import pygame as engine
import OpenGL.GL as gl
import imgui
from imgui.integrations.pygame import PygameRenderer

version = "v05.04.2023"

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
        self.__render_callbacks : List[Callable] = []
        # Callbacks during tick time (before any rendering).
        self.__tick_callbacks : List[Callable] = []
        
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
            
        self.__imgui_renderer.shutdown()
        engine.quit()
        sys.exit()
            
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
        gl.glClearColor(self.__cls_color[0], self.__cls_color[1], self.__cls_color[2], self.__cls_color[3])
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
    def __render(self):
        """ Render the current state of the applet.
        """
        # Draw ImGui data to renderer.
        imgui.render()
        self.__imgui_renderer.render(imgui.get_draw_data())
        # Custom Pygame render callbacks.
        for callback in self.__render_callbacks:
            callback(screen = self.__screen)
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

    def register_pygame_render_callback(self, callback : Callable):
        """ Register a callback to be called during Pygame render time.
        """
        self.__render_callbacks.append(callback)
        
    def register_tick_callback(self, callback : Callable):
        """ Regsiter a callback to be called during the Applet's tick stage (before rendering, after input.)
        """
        self.__tick_callbacks.append(callback)
    
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
