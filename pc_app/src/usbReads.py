import os
import tkinter as tk
from tkinter import ttk
import pygame  # Reintroduce pygame for controller input handling

pygame.init()  # Initialize pygame globally

# Define 20 global variables
global_vars = [0] * 20

def assign_key(index, key_assignments, status_label, root):
    """
    Opens a popup window to capture a key press and assigns it to a global variable.
    Updates the KEY_ASSIGNMENTS environment variable.
    """
    def capture_key():
        """
        Captures the key press in the popup window.
        """
        popup = tk.Toplevel(root)
        popup.title("Assign Key")
        popup.geometry("300x200")
        popup.resizable(False, False)

        label = tk.Label(popup, text=f"Press a key to assign to Global Var {index + 1}", font=("Arial", 12))
        label.pack(pady=10)

        # Dropdown to select input type
        input_type_var = tk.StringVar(value="Button")
        input_type_label = tk.Label(popup, text="Select Input Type:")
        input_type_label.pack(pady=5)
        input_type_dropdown = ttk.Combobox(popup, textvariable=input_type_var, values=["Button", "Joystick"], state="readonly")
        input_type_dropdown.pack(pady=5)

        def key_event_handler(event):
            """
            Handles key press events in the popup window.
            """
            key_name = event.keysym  # Get the key name from the event
            input_type = input_type_var.get()  # Get the selected input type

            key_assignments[index].config(state="normal")  # Enable the Entry widget
            key_assignments[index].delete(0, "end")  # Clear the current value
            key_assignments[index].insert(0, f"{key_name} ({input_type})")  # Insert the new key name with input type
            key_assignments[index].config(state="readonly")  # Set the Entry widget back to readonly

            # Update the KEY_ASSIGNMENTS environment variable
            current_assignments = eval(os.environ.get('KEY_ASSIGNMENTS', "{}"))
            current_assignments[f"global_var_{index}"] = {"key": key_name, "type": input_type}
            os.environ['KEY_ASSIGNMENTS'] = str(current_assignments)

            # Debug log for key assignments
            print(f"[DEBUG] Updated KEY_ASSIGNMENTS: {os.environ['KEY_ASSIGNMENTS']}")

            popup.destroy()  # Close the popup window
            root.focus_force()  # Return focus to the main Tkinter application

        # Bind key press events to the popup window
        popup.bind("<KeyPress>", key_event_handler)

        # Focus the popup window
        popup.focus_force()

    capture_key()