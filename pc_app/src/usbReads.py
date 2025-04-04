import pygame

def detect_ps5_controller():
    pygame.joystick.init()
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

def detect_keyboard_events(events):
    """
    Detects keyboard events from a list of pygame events and returns a list of messages for key presses/releases.
    """
    messages = []
    for event in events:
        if event.type == pygame.KEYDOWN:
            messages.append(f"Key '{pygame.key.name(event.key)}' pressed.")
        elif event.type == pygame.KEYUP:
            messages.append(f"Key '{pygame.key.name(event.key)}' released.")
    return messages

def read_keyboard_inputs():
    """
    Reads keyboard inputs and returns a list of messages for key presses/releases.
    """
    events = pygame.event.get()
    return detect_keyboard_events(events)

def read_controller_inputs(joystick):
    """
    Reads PS5 controller inputs and returns a list of messages for button presses/releases, axis motions, and hat motions.
    """
    messages = []
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYBUTTONDOWN:
            messages.append(f"Controller Button {event.button} pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            messages.append(f"Controller Button {event.button} released.")
        elif event.type == pygame.JOYAXISMOTION:
            messages.append(f"Controller Axis {event.axis} moved to {event.value:.1f}.")
        elif event.type == pygame.JOYHATMOTION:
            messages.append(f"Controller Hat {event.hat} moved to {event.value}.")
    return messages
