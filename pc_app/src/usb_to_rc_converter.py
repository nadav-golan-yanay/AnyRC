import pygame
from src.usbController import detect_ps5_controller

class USBToRCConverter:
    def __init__(self):
        self.channels = [1500] * 8  # Initialize 8 channels with neutral PWM value
        self.joystick, self.controller_message = detect_ps5_controller()
        pygame.init()

    def get_channels(self):
        return self.channels

    def get_channels_display(self):
        return " | ".join([f"Ch{i+1}: {value}" for i, value in enumerate(self.channels)])

    def update_channels(self, new_channels):
        """
        Updates the channel values.
        """
        if len(new_channels) == len(self.channels):
            self.channels = new_channels
