import pygame

try:
    pygame.init()
    if pygame.get_init():
        print("Pygame initialized successfully.")
    else:
        print("Pygame initialization failed.")
except pygame.error as e:
    print(f"Pygame initialization error: {e}")

# Test event loop
try:
    pygame.event.pump()
    print("Pygame event loop is responsive.")
except pygame.error as e:
    print(f"Pygame event loop error: {e}")

pygame.quit()
