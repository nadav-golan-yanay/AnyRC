import os
import pygame
import tkinter as tk
from tkinter import ttk
from src.usbReads import detect_ps5_controller, read_keyboard_inputs, read_controller_inputs

class PS5ControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PS5 Controller App")
        self.root.geometry("400x300")

        # Initialize pygame
        pygame.init()

        # Create UI elements
        self.status_label = ttk.Label(root, text="Status: Waiting for controller...", wraplength=380)
        self.status_label.pack(pady=10)

        self.input_display = tk.Text(root, height=10, width=45, state="disabled")
        self.input_display.pack(pady=10)

        self.start_button = ttk.Button(root, text="Start Reading Inputs", command=self.start_reading_inputs)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Reading Inputs", command=self.stop_reading_inputs, state="disabled")
        self.stop_button.pack(pady=10)

        self.close_button = ttk.Button(root, text="Close", command=self.close_app)
        self.close_button.pack(pady=10)

        self.input_mode = tk.StringVar(value="Controller")  # Default to Controller

        # Add input mode selection
        self.input_mode_label = ttk.Label(root, text="Select Input Mode:")
        self.input_mode_label.pack(pady=5)

        self.input_mode_selector = ttk.Combobox(root, textvariable=self.input_mode, values=["Controller", "Keyboard"], state="readonly")
        self.input_mode_selector.pack(pady=5)

        self.running = False
        self.joystick = None

    def start_reading_inputs(self):
        if self.input_mode.get() == "Controller":
            self.joystick, status_message = detect_ps5_controller()
            self.status_label.config(text=f"Status: {status_message}")
            if not self.joystick:
                return
        else:
            self.status_label.config(text="Status: Reading keyboard inputs.")

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.read_inputs()

    def stop_reading_inputs(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped reading inputs.")

    def read_inputs(self):
        if not self.running:
            return

        if self.input_mode.get() == "Controller" and self.joystick:
            messages = read_controller_inputs(self.joystick)
        elif self.input_mode.get() == "Keyboard":
            os.environ['SDL_VIDEO_WINDOW_POS'] = "-1000,-1000"  # Move the window off-screen
            pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Create a 1x1 borderless window
            messages = read_keyboard_inputs()
        else:
            messages = []

        for message in messages:
            self.log_input(message)

        # Schedule the next read
        self.root.after(50, self.read_inputs)

    def log_input(self, message):
        self.input_display.config(state="normal")
        self.input_display.insert("end", message + "\n")
        self.input_display.see("end")
        self.input_display.config(state="disabled")

    def close_app(self):
        self.running = False
        pygame.quit()
        self.root.destroy()
