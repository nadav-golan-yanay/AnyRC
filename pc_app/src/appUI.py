import os
import importlib
import tkinter as tk
import pygame  # Import pygame module
import tkinter.messagebox as messagebox
from tkinter import ttk, Frame
from src.usbController import list_available_devices
from src.usb_to_rc_converter import USBToRCConverter
from src import process  # Import the process module
from usb_comm import USBComm  # Ensure USBComm is imported
import gc  # Add at top with other imports
import time

class AnyRC:
    def __init__(self, root):
        self.root = root
        self.root.title("AnyRC Controller")
        
        # Set application icon with correct path
        icon_path = r"C:\Users\nadav\OneDrive\Desktop\RealSIm5.0\pc_app\Icon\AnyRC_Icon.png"
        try:
            icon = tk.PhotoImage(file=icon_path, format="png")
            self.root.iconphoto(False, icon)
            self._icon = icon  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Failed to load icon from {icon_path}: {e}")
        
        # Create a frame for USB status and search button
        self.usb_frame = ttk.Frame(self.root)
        self.usb_frame.pack(fill='x', pady=5)
        
        # Add USB status label
        self.usb_status_label = ttk.Label(self.usb_frame, text="USB Status: Disconnected", font=("Arial", 10))
        self.usb_status_label.pack(side='left', padx=5)
        
        # Add Search USB button
        self.search_usb_button = ttk.Button(self.usb_frame, text="Search USB", command=self.search_usb)
        self.search_usb_button.pack(side='right', padx=5)
        
        self.usb_comm = None
        self.setup_usb_comm()  # Setup USB communication immediately

        self.rc_converter = USBToRCConverter()  # Initialize the RC converter
        self.process_module = process  # Store the process module
        self.process = process.Process()  # Initialize the Process class

        processor_file = r"C:\Users\nadav\OneDrive\Desktop\RealSIm5.0\pc_app\src\process.py"
        self.processor_file = processor_file  # Store the processor file path
        self.processor_last_modified = os.path.getmtime(self.processor_file)  # Track last modified time

        self.main_frame = Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Add table headers
        headers = ["Device", "Assign Input", "Assigned Input", "Input"]
        for col, header in enumerate(headers):
            label = ttk.Label(self.table_frame, text=header, font=("Arial", 10, "bold"))
            label.grid(row=0, column=col, padx=5, pady=5)

        self.rows = []
        for i in range(20):  # 20 rows for global variables
            row = {}

            # Device dropdown menu
            available_devices = list_available_devices()  # Get all available devices
            row["device"] = ttk.Combobox(self.table_frame, values=available_devices, state="readonly", width=20)
            row["device"].set("Keyboard")  # Default to Keyboard
            row["device"].grid(row=i + 1, column=0, padx=5, pady=5)

            # Assign input button
            row["assign_button"] = ttk.Button(self.table_frame, text="Assign Input", 
                                              command=lambda r=row: self.assign_input(r))
            row["assign_button"].grid(row=i + 1, column=1, padx=5, pady=5)

            # Assigned input display with explicit style
            row["assigned_input"] = ttk.Entry(self.table_frame, width=15)
            row["assigned_input"].configure(state="readonly", style="Default.TEntry")
            row["assigned_input"].grid(row=i + 1, column=2, padx=5, pady=5)

            # Input display
            row["input_display"] = ttk.Entry(self.table_frame, state="readonly", width=15)
            row["input_display"].grid(row=i + 1, column=3, padx=5, pady=5)

            self.rows.append(row)

        # Configure styles before creating widgets
        self.style = ttk.Style()
        self.style.configure("Assigned.TEntry", fieldbackground="pale green")
        self.style.configure("Default.TEntry", fieldbackground="white")

        # RC Channels Window
        self.rc_window = ttk.LabelFrame(self.main_frame, text="RC Channels")
        self.rc_window.pack(side="right", fill="y", padx=10, pady=10)

        self.rc_display = tk.Text(self.rc_window, height=30, width=50, state="disabled")  # Increased size
        self.rc_display.pack(padx=10, pady=10)

        # Add global Start/Stop Read buttons
        self.start_read_button = ttk.Button(self.main_frame, text="Start Read", command=self.start_read)
        self.start_read_button.pack(side="left", padx=10, pady=10)

        self.stop_read_button = ttk.Button(self.main_frame, text="Stop Read", command=self.stop_read)
        self.stop_read_button.pack(side="left", padx=10, pady=10)

        self.close_button = ttk.Button(self.main_frame, text="Close", command=self.close_app)
        self.close_button.pack(pady=10)

        # Add a button to open the processor file
        self.edit_processor_button = ttk.Button(self.main_frame, text="Edit Processor File", command=self.open_processor_file)
        self.edit_processor_button.pack(pady=10)

        self.current_row = None  # Track the row for which input is being assigned
        self.reading_inputs = False  # Track whether input reading is active
        self.last_gc_time = time.time()
        self.update_interval = 100  # 100ms for UI updates
        self.gc_interval = 60  # Run garbage collection every 60 seconds
        self.update_rc_display_periodically()  # Now safe to call this
        self.mouse_motion_active = False
        self.mouse_assigned_rows = []  # Track rows with mouse assignments

    def set_usb_comm(self, usb_comm):
        """
        Sets the USBComm instance for sending RC channels.
        """
        self.usb_comm = usb_comm

    def setup_usb_comm(self):
        """
        Detects and connects to the Arduino. Shows selection dialog if multiple devices found.
        """
        arduino_ports = USBComm.list_arduino_ports()
        
        if not arduino_ports:
            self.usb_status_label.config(text="USB Status: No Arduino found", foreground="red")
            return
            
        if len(arduino_ports) == 1:
            port = arduino_ports[0]['device']
        else:
            # Create selection dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Arduino Device")
            dialog.geometry("400x200")
            dialog.transient(self.root)
            dialog.grab_set()
            
            selected_port = tk.StringVar()
            
            def on_select():
                dialog.destroy()
            
            ttk.Label(dialog, text="Multiple Arduino devices found.\nPlease select one:").pack(pady=10)
            
            for port_info in arduino_ports:
                text = f"{port_info['device']} - {port_info['description']}"
                ttk.Radiobutton(dialog, text=text, value=port_info['device'], 
                              variable=selected_port).pack(pady=5)
            
            ttk.Button(dialog, text="Connect", command=on_select).pack(pady=10)
            
            self.root.wait_window(dialog)
            port = selected_port.get()
            
            if not port:  # User closed dialog without selecting
                return
        
        self.usb_comm = USBComm(port=port)
        if self.usb_comm.connect():
            self.usb_status_label.config(text=f"USB Status: Connected to {port}", foreground="green")
        else:
            self.usb_status_label.config(text=f"USB Status: Failed to connect to {port}", foreground="red")

    def search_usb(self):
        """
        Searches for USB devices and attempts to reconnect.
        """
        if self.usb_comm:
            self.usb_comm.disconnect()
        
        self.setup_usb_comm()
        self.update_usb_status()

    def open_processor_file(self):
        """
        Opens the processor file in the default text editor.
        """
        try:
            os.system(f"notepad {self.processor_file}")  # Open the processor file in Notepad
        except Exception:
            pass

    def update_rc_display(self):
        """
        Updates the RC channel display in the UI.
        """
        # Fetch the latest RC channel values from the Process class
        channels_display = self.process.get_rc_channels_display()  # Get RC channel display as a string
        self.rc_display.config(state="normal")
        self.rc_display.delete("1.0", "end")  # Clear the RC display
        self.rc_display.insert("end", channels_display)  # Insert the updated RC channel values
        self.rc_display.config(state="disabled")  # Make the RC display read-only

        # Send RC channels to the Arduino if USBComm is set
        if self.usb_comm:
            self.usb_comm.send_rc_channels(self.process.get_rc_channels())

    def update_usb_status(self):
        """
        Updates the USB connection status label.
        """
        if self.usb_comm and self.usb_comm.serial_connection and self.usb_comm.serial_connection.is_open:
            self.usb_status_label.config(text="USB Status: Connected", foreground="green")
        else:
            self.usb_status_label.config(text="USB Status: Disconnected", foreground="red")
        self.root.after(1000, self.update_usb_status)  # Check every second

    def update_rc_display_periodically(self):
        """
        Periodically updates the RC channel display and handles garbage collection.
        """
        try:
            current_time = time.time()
            
            # Run garbage collection periodically
            if current_time - self.last_gc_time > self.gc_interval:
                gc.collect()
                self.last_gc_time = current_time

            self.update_rc_display()
            
            # Schedule next update using weak reference to prevent circular references
            self.root.after(self.update_interval, lambda: self.update_rc_display_periodically() 
                          if self.root.winfo_exists() else None)
        except Exception as e:
            print(f"Error in update_rc_display_periodically: {e}")
            # Try to recover by scheduling next update
            self.root.after(self.update_interval, self.update_rc_display_periodically)

    def close_app(self):
        """
        Properly cleanup resources before closing.
        """
        self.reading_inputs = False  # Stop input processing
        if self.usb_comm:
            self.usb_comm.disconnect()
        
        # Clear any scheduled updates
        self.root.after_cancel(self.root.after(1))
        
        # Force garbage collection before closing
        gc.collect()
        
        self.root.destroy()

    def assign_input(self, row):
        """
        Assigns an input to the selected device.
        """
        selected_device = row["device"].get()
        if not selected_device:
            return

        self.current_row = row
        # Explicitly set the style to show assignment mode
        row["assigned_input"].configure(style="Assigned.TEntry")

        if selected_device == "Keyboard":
            self.root.bind("<KeyPress>", self.capture_key)
        elif selected_device == "Mouse":
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Mouse Input")
            dialog.geometry("300x250")
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(dialog, text="Select mouse input type:").pack(pady=10)
            
            selected_type = tk.StringVar(value="")
            
            input_types = [
                ("Left Button", "Button-1"),
                ("Middle Button", "Button-2"),
                ("Right Button", "Button-3"),
                ("X Movement", "Motion-X"),
                ("Y Movement", "Motion-Y"),
                ("Wheel", "MouseWheel")
            ]

            for text, value in input_types:
                ttk.Radiobutton(dialog, text=text, value=value, 
                              variable=selected_type).pack(pady=5)

            def confirm_selection():
                input_type = selected_type.get()
                if input_type:
                    dialog.destroy()  # Close dialog first
                    self.capture_mouse_input(None, input_type)  # Then capture input
                else:
                    # If no selection, reset the style
                    self.current_row["assigned_input"].configure(style="Default.TEntry")

            ttk.Button(dialog, text="Assign", command=confirm_selection).pack(pady=10)
            
            def on_dialog_close():
                # Reset style when dialog is closed without selection
                self.current_row["assigned_input"].configure(style="Default.TEntry")
                self.current_row = None
                dialog.destroy()
                
            dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)

    def capture_key(self, event):
        if self.current_row:
            assigned_input = event.keysym
            self.current_row["assigned_input"].config(state="normal")
            self.current_row["assigned_input"].delete(0, "end")
            self.current_row["assigned_input"].insert(0, assigned_input)
            self.current_row["assigned_input"].config(state="readonly")
            self.root.unbind("<KeyPress>")
            self.current_row = None

    def capture_mouse_input(self, event, input_type):
        """
        Captures mouse input for assignment.
        """
        if self.current_row:
            try:
                self.current_row["assigned_input"].config(state="normal")
                self.current_row["assigned_input"].delete(0, "end")
                self.current_row["assigned_input"].insert(0, input_type)
                self.current_row["assigned_input"].config(state="readonly")
                
                # Add row to mouse tracking if it's a motion event
                if "Motion" in input_type or input_type == "MouseWheel":
                    self.mouse_motion_active = True
                    if self.current_row not in self.mouse_assigned_rows:
                        self.mouse_assigned_rows.append(self.current_row)
                
                # Reset style after successful assignment
                self.current_row["assigned_input"].configure(style="Default.TEntry")
                self.current_row = None
            except Exception as e:
                print(f"Error in capture_mouse_input: {e}")
                self.current_row["assigned_input"].configure(style="Default.TEntry")
                self.current_row = None

    def start_read(self):
        """
        Starts reading input for all devices.
        """
        if self.reading_inputs:
            return

        self.reading_inputs = True
        self.root.bind("<KeyPress>", self.read_keyboard_input)  # Bind key press events
        self.root.bind("<KeyRelease>", self.read_keyboard_release)  # Bind key release events
        # Add mouse bindings
        self.root.bind("<Button-1>", self.read_mouse_input)
        self.root.bind("<Button-2>", self.read_mouse_input)
        self.root.bind("<Button-3>", self.read_mouse_input)
        self.root.bind("<ButtonRelease-1>", self.read_mouse_release)
        self.root.bind("<ButtonRelease-2>", self.read_mouse_release)
        self.root.bind("<ButtonRelease-3>", self.read_mouse_release)
        if self.mouse_motion_active:
            self.root.bind("<Motion>", self.read_mouse_motion)
            self.root.bind("<MouseWheel>", self.read_mouse_motion)
        self.update_process_inputs()  # Start sending inputs to the process

    def stop_read(self):
        """
        Stops reading input for all devices.
        """
        if not self.reading_inputs:
            return

        self.reading_inputs = False
        self.root.unbind("<KeyPress>")  # Unbind key press events
        self.root.unbind("<KeyRelease>")  # Unbind key release events
        # Unbind mouse events
        self.root.unbind("<Button-1>")
        self.root.unbind("<Button-2>")
        self.root.unbind("<Button-3>")
        self.root.unbind("<ButtonRelease-1>")
        self.root.unbind("<ButtonRelease-2>")
        self.root.unbind("<ButtonRelease-3>")
        self.root.unbind("<Motion>")
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<MouseWheel>")

    def reload_process_module(self):
        """
        Reloads the process module if it has been modified.
        """
        try:
            current_modified = os.path.getmtime(self.processor_file)
            if current_modified != self.processor_last_modified:
                self.processor_last_modified = current_modified
                importlib.reload(self.process_module)  # Reload the process module
                self.process = self.process_module.Process()  # Reinitialize the Process class
        except Exception:
            pass

    def update_process_inputs(self):
        """
        Periodically sends inputs to the Process class with optimized frequency.
        """
        if not self.reading_inputs:
            return

        try:
            self.reload_process_module()
            inputs = []
            for row in self.rows[:8]:
                input_value = row["input_display"].get()
                inputs.append(int(input_value) if input_value.isdigit() else 0)

            # Pad with zeros if needed
            inputs.extend([0] * (8 - len(inputs)))

            self.process.update_ui_inputs(inputs)
            self.process.process_inputs()

            # Schedule next update only if still reading inputs
            if self.reading_inputs and self.root.winfo_exists():
                self.root.after(self.update_interval, self.update_process_inputs)
        except Exception as e:
            print(f"Error in update_process_inputs: {e}")
            if self.reading_inputs and self.root.winfo_exists():
                self.root.after(self.update_interval, self.update_process_inputs)

    def read_keyboard_input(self, event):
        """
        Reads input from the keyboard and updates the corresponding input display when a key is pressed.
        """
        key_pressed = event.keysym  # Get the key symbol (e.g., "a", "Shift")

        # Update the input display only for rows where the key has been assigned
        for row in self.rows:
            assigned_key = row["assigned_input"].get()
            if assigned_key == key_pressed:  # Check if the pressed key matches the assigned key
                row["input_display"].config(state="normal")
                row["input_display"].delete(0, "end")
                row["input_display"].insert(0, 1)  # Button pressed, value is 1
                row["input_display"].config(state="readonly")

    def read_keyboard_release(self, event):
        """
        Reads input from the keyboard and updates the corresponding input display when a key is released.
        """
        key_released = event.keysym  # Get the key symbol (e.g., "a", "Shift")

        # Update the input display only for rows where the key has been assigned
        for row in self.rows:
            assigned_key = row["assigned_input"].get()
            if assigned_key == key_released:  # Check if the released key matches the assigned key
                row["input_display"].config(state="normal")
                row["input_display"].delete(0, "end")
                row["input_display"].insert(0, 0)  # Button released, value is 0
                row["input_display"].config(state="readonly")

    def read_joystick_input(self):
        """
        Reads input from the joystick and updates the corresponding input display.
        """
        if not self.rc_converter.joystick:
            return

        self.rc_converter.joystick.init()
        pygame.event.pump()  # Process joystick events

        # Map joystick axis values to 1000-2000 range
        for row in self.rows:
            if row["device"].get() == self.rc_converter.joystick.get_name():
                axis_value = self.rc_converter.joystick.get_axis(0)  # Example: Read axis 0
                mapped_value = int(1000 + (axis_value + 1) * 500)  # Map -1 to 1 range to 1000-2000
                row["input_display"].config(state="normal")
                row["input_display"].delete(0, "end")
                row["input_display"].insert(0, mapped_value)
                row["input_display"].config(state="readonly")

    def read_mouse_input(self, event):
        """
        Handles mouse button press events.
        """
        input_type = f"Button-{event.num}"
        for row in self.rows:
            if row["device"].get() == "Mouse" and row["assigned_input"].get() == input_type:
                row["input_display"].config(state="normal")
                row["input_display"].delete(0, "end")
                row["input_display"].insert(0, "1")
                row["input_display"].config(state="readonly")

    def read_mouse_release(self, event):
        """
        Handles mouse button release events.
        """
        input_type = f"Button-{event.num}"
        for row in self.rows:
            if row["device"].get() == "Mouse" and row["assigned_input"].get() == input_type:
                row["input_display"].config(state="normal")
                row["input_display"].delete(0, "end")
                row["input_display"].insert(0, "0")
                row["input_display"].config(state="readonly")

    def read_mouse_motion(self, event):
        """
        Handles mouse motion events and wheel events.
        """
        for row in self.mouse_assigned_rows:
            if row["device"].get() == "Mouse":
                input_type = row["assigned_input"].get()
                value = 1500  # Default center value

                if input_type == "Motion-X":
                    value = int(1000 + (event.x / self.root.winfo_width()) * 1000)
                elif input_type == "Motion-Y":
                    value = int(1000 + (event.y / self.root.winfo_height()) * 1000)
                elif input_type == "MouseWheel" and hasattr(event, 'delta'):
                    # Mouse wheel movement (delta is typically ±120)
                    current_value = int(row["input_display"].get() or 1500)
                    wheel_sensitivity = 50  # Adjust this value to change sensitivity
                    delta = event.delta / 120 * wheel_sensitivity
                    value = max(1000, min(2000, current_value + delta))
                
                row["input_display"].config(state="normal")
                row["input_display"].delete(0, "end")
                row["input_display"].insert(0, str(int(value)))
                row["input_display"].config(state="readonly")
