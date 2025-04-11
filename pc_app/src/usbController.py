import pygame

pygame.init()  # Initialize pygame globally

def detect_ps5_controller():
    """
    Detects a connected PS5 controller and returns the joystick object and a status message.
    """
    pygame.joystick.init()  # Initialize the joystick module
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        return None, "No controllers detected."

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        controller_name = joystick.get_name()
        if "PS5" in controller_name or "DualSense" in controller_name:
            return joystick, f"PS5 Controller detected ({controller_name})."

    return None, "No PS5 Controller detected."

def list_available_devices():
    """
    Lists all available input devices (controllers, keyboard, and mouse).
    """
    pygame.joystick.init()  # Initialize the joystick module
    devices = ["Keyboard", "Mouse"]  # Always include the keyboard and mouse as options

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        devices.append(joystick.get_name())  # Add each joystick name to the list

    return devices
