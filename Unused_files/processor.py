import os
import pygame
from src.usb_to_rc_converter import USBToRCConverter
from src.usbReads import read_inputs_and_update_globals, global_vars

class Processor:
    def __init__(self, input_mode="Keyboard", joystick=None, root=None, processor_file=None):
        """
        Initializes the Processor with the input mode and optional joystick or root window.
        :param input_mode: "Keyboard" or "Controller"
        :param joystick: Pygame joystick object (if input_mode is "Controller")
        :param root: Tkinter root window (if input_mode is "Keyboard")
        :param processor_file: Path to the user-defined processor file
        """
        self.input_mode = input_mode
        self.joystick = joystick
        self.root = root
        self.rc_converter = USBToRCConverter()  # Initialize the RC converter
        self.processor_file = processor_file  # Path to the processor file
        pygame.init()

        # Ensure the processor file exists
        self.ensure_processor_file()

    def ensure_processor_file(self):
        """
        Creates or updates the processor file with a default template.
        """
        if self.processor_file:
            try:
                with open(self.processor_file, "w") as file:
                    file.write(
                        "processor file\n\n"
                        "setup:\n"
                        "    input1 = usbread1\n"
                        "    input2 = usbread2\n"
                        "    input3 = usbread3\n"
                        "    input4 = usbread4\n"
                        "    input5 = usbread5\n"
                        "    input6 = usbread6\n"
                        "    input7 = usbread7\n"
                        "    input8 = usbread8\n"
                        "    input9 = usbread9\n"
                        "    input10 = usbread10\n"
                        "    input11 = usbread11\n"
                        "    input12 = usbread12\n"
                        "    input13 = usbread13\n"
                        "    input14 = usbread14\n"
                        "    input15 = usbread15\n"
                        "    input16 = usbread16\n"
                        "    input17 = usbread17\n"
                        "    input18 = usbread18\n"
                        "    input19 = usbread19\n"
                        "    input20 = usbread20\n\n"
                        "main:\n"
                        "    RC_channel1 = input1\n"
                        "    RC_channel2 = input2\n"
                        "    RC_channel3 = input3 + input4\n"
                        "    RC_channel4 = (input5 + input6) / 2\n"
                    )
                print(f"[INFO] Processor file updated at {self.processor_file}")
            except Exception as e:
                print(f"[ERROR] Failed to update processor file: {e}")

    def process_inputs(self):
        """
        Processes inputs and computes RC channels.
        :return: List of RC channel values.
        """
        # Step 1: Read inputs
        if self.input_mode == "Controller" and self.joystick:
            read_inputs_and_update_globals("Controller", joystick=self.joystick)
        elif self.input_mode == "Keyboard" and self.root:
            read_inputs_and_update_globals("Keyboard", root=self.root)

        # Step 2: Process inputs using the processor file
        rc_channels = self.execute_processor_file()

        # Step 3: Update RC channels in the RC converter
        self.rc_converter.channels = rc_channels

        return self.rc_converter.get_channels()

    def execute_processor_file(self):
        """
        Reads and executes the logic defined in the processor file.
        :return: List of RC channel values.
        """
        rc_channels = [1500] * 8  # Initialize RC channels with neutral PWM values
        local_vars = {"global_vars": global_vars, "rc_channels": rc_channels}

        # Dynamically map input1, input2, ..., input20 to global_vars[0], global_vars[1], ..., global_vars[19]
        for i in range(20):
            local_vars[f"input{i + 1}"] = global_vars[i]

        if not self.processor_file or not os.path.exists(self.processor_file):
            print("[ERROR] Processor file not specified or does not exist.")
            return rc_channels

        try:
            with open(self.processor_file, "r") as file:
                lines = file.readlines()

            # Parse and execute the setup and main sections
            in_main_section = False
            block = []  # To store lines of a block
            for line in lines:
                line = line.rstrip()  # Preserve indentation but remove trailing whitespace
                # Skip non-executable lines
                if not line or line.startswith("#"):
                    continue
                if line.startswith("setup:"):
                    in_main_section = False
                    continue
                elif line.startswith("main:"):
                    in_main_section = True
                    continue

                # Add line to the current block
                block.append(line)

                # If the line is not indented or ends a block, execute the block
                if not line.startswith(" ") and block:
                    try:
                        # Normalize indentation for the block
                        normalized_block = "\n".join(line.lstrip() for line in block)
                        print(f"[DEBUG] Executing block:\n{normalized_block}")  # Log the block being executed
                        exec(normalized_block, {}, local_vars)  # Execute the block
                    except Exception as e:
                        print(f"[ERROR] Failed to execute block:\n{normalized_block}")
                        print(f"[ERROR] {e}")
                        break  # Stop execution on error
                    finally:
                        block = []  # Reset the block

            # Execute any remaining block
            if block:
                try:
                    # Normalize indentation for the block
                    normalized_block = "\n".join(line.lstrip() for line in block)
                    print(f"[DEBUG] Executing block:\n{normalized_block}")  # Log the block being executed
                    exec(normalized_block, {}, local_vars)  # Execute the block
                except Exception as e:
                    print(f"[ERROR] Failed to execute block:\n{normalized_block}")
                    print(f"[ERROR] {e}")

        except Exception as e:
            print(f"[ERROR] Failed to read processor file: {e}")

        return local_vars["rc_channels"]

    def edit_processing_logic(self):
        """
        Opens the processor file for editing so the user can modify the logic.
        """
        if not self.processor_file:
            print("[ERROR] Processor file not specified.")
            return

        try:
            os.system(f"notepad {self.processor_file}")  # Open the processor file in Notepad
        except Exception as e:
            print(f"[ERROR] Unable to open processor file for editing: {e}")
