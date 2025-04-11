import pygame

def main():
    pygame.init()  # Initialize pygame
    pygame.display.set_mode((300, 100))  # Create a small visible window
    pygame.display.set_caption("Keyboard Test")

    # Define the keys to display
    selected_keys = ["w", "a", "s", "d", "space", "up", "down", "left", "right"]

    print("Press keys to test keyboard input. Only selected keys will be displayed.")
    print(f"Selected keys: {selected_keys}")
    print("Close the window to exit.")

    running = True
    while running:
        pygame.event.pump()  # Process events
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False  # Exit the loop when the window is closed
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if key_name in selected_keys:
                    print(f"Key pressed: {key_name}")  # Log key press
            elif event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                if key_name in selected_keys:
                    print(f"Key released: {key_name}")  # Log key release

    pygame.quit()  # Quit pygame when the loop ends

if __name__ == "__main__":
    main()
