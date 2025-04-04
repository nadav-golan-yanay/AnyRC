import os
import pygame
from pc_app.src.usbReads import read_keyboard_inputs

def main():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "-1000,-1000"  # Move the window off-screen
    pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Create a 1x1 borderless window

    try:
        while True:
            # Detect keyboard events
            keyboard_messages = read_keyboard_inputs()
            for message in keyboard_messages:
                print(message)

            pygame.time.delay(100)  # Delay to prevent high CPU usage
    except KeyboardInterrupt:
        print("Exiting...")
        pygame.quit()

if __name__ == "__main__":
    main()
