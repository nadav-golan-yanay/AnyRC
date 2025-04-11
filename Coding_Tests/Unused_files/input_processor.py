import pygame
from src.usb_to_rc_converter import USBToRCConverter
from src.usbReads import read_inputs_and_update_globals, global_vars

class InputProcessor:
    def __init__(self, input_mode="Keyboard", joystick=None, root=None):
        """
        Initializes the InputProcessor with the input mode and optional joystick or root window.
        :param input_mode: "Keyboard" or "Controller"
        :param joystick: Pygame joystick object (if input_mode is "Controller")
        :param root: Tkinter root window (if input_mode is "Keyboard")
        """
        self.input_mode = input_mode
        self.joystick = joystick
        self.root = root
        self.rc_converter = USBToRCConverter()  # Initialize the RC converter
        pygame.init()

    def process_inputs(self):
        """
        Processes inputs from the selected input mode and updates RC channels.
        :return: List of RC channel values.
        """
        # Update global variables based on the input mode
        if self.input_mode == "Controller" and self.joystick:
            read_inputs_and_update_globals("Controller", joystick=self.joystick)
        elif self.input_mode == "Keyboard" and self.root:
            read_inputs_and_update_globals("Keyboard", root=self.root)

        # Update RC channels using the USBToRCConverter
        self.rc_converter.update_channels()

        # Return the computed RC channels
        return self.rc_converter.get_channels()
