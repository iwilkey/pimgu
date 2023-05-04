# Pimgu

Pimgu is a lightweight framework that combines the power of Pygame and ImGui to create intuitive and responsive 2D GUI applications. This framework provides an easy-to-use interface to build user interfaces while harnessing the capabilities of Pygame and ImGui under the hood.

## Features

- Simple API for creating and managing ImGui-based user interfaces
- Integrated with Pygame for efficient event handling and rendering
- Customizable callbacks for input handling, ImGui rendering, and Pygame rendering
- Easy control of application flow and frame rate
- Cross-platform support

## Installation

It is recommended that you have <= Python 3.6 installed on your machine.

``` bash
pip install pimgu
```

## Usage

Here's a basic example of how to create a Pimgu application with a simple ImGui window:

``` python
import imgui
from pimgu import Applet

def main_gui():
    imgui.begin("My First Pimgu Window")
    imgui.text("Hello, world!")
    imgui.end()

if __name__ == "__main__":
    app = Applet(title="Pimgu Example")
    app.register_imgui_callback(main_gui)
    app.run()
```

## Documentation

### Applet

The core class of Pimgu is Applet, which provides a high-level interface to manage your application.

#### Applet Constructor

Create a new Applet instance with the following parameters:

- title (str, optional): The title of the application window. Default is "Pimgu Application".
- dimensions (tuple, optional): The dimensions of the window (width, height). Default is (1280, 720).
- icon_path (str, optional): Path to the window icon (optional). Default is an empty string.

#### Applet Methods

- `run()`: Runs the main loop of the application.
- `register_input_callback(callback: Callable)`: Register a callback to be called during Applet input processing.
- `register_imgui_callback(callback: Callable)`: Register a callback to be called during Applet GUI processing.
- `register_pygame_render_callback(callback: Callable)`: Register a callback to be called during Pygame render time.
- `register_tick_callback(callback: Callable)`: Register a callback to be called during the Applet's tick stage (before rendering, after input).

#### Applet Properties

- `get_title()` -> str: Get the title of the application window.
- `get_screen()` -> pygame.Surface: Get the Pygame screen surface.
- `get_imgui_io()`: Get the ImGui IO buffer.
- `get_imgui_renderer()` -> PygameRenderer: Get the ImGui Pygame renderer.
- `get_clock()` -> pygame.time.Clock: Get the Pygame clock object.
- `get_cls_color()` -> tuple: Get the clear color of the OpenGL buffer.
- `is_running()` -> bool: Check if the application is running.
- `get_target_fps()` -> int: Get the target frame rate.
- `set_cls_color(cls_color: tuple)`: Set the clear color of the OpenGL buffer.
- `set_running(running: bool)`: Set the application running state.
- `set_target_fps(target_fps: int)`: Set the target frame rate.

### Examples

You can find more examples in the examples folder, which demonstrate various features of Pimgu, such as handling input events, custom rendering, and ImGui usage.

### Contributing

Contributions are welcome! Feel free to submit issues or pull requests to help improve Pimgu.

### License

Pimgu is released under the MIT License. See the `LICENSE` file for more information.

### Contact

This project is developed and maintained by Ian Wilkey (iwilkey). Feel free to contact him through his website, https://www.iwilkey.com/contact, with any questions, concerns, ideas, or issues.