import pygame

def main():
    pygame.init()  # Initialize pygame
    pygame.joystick.init()  # Initialize the joystick module

    # Detect and initialize the first connected joystick
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No controllers detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller detected: {joystick.get_name()}")

    print("Press buttons or move axes on the controller. Close the window to exit.")

    running = True
    while running:
        pygame.event.pump()  # Process events
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False  # Exit the loop when the window is closed
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released.")
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Axis {event.axis} moved to {event.value:.2f}.")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Hat {event.hat} moved to {event.value}.")

    pygame.quit()  # Quit pygame when the loop ends

if __name__ == "__main__":
    main()
