from src.usb_to_rc_converter import USBToRCConverter

class Process:
    def __init__(self):
        """
        Initializes the Process class.
        """
        self.rc_converter = USBToRCConverter()  # Initialize the RC converter
        self.rc_channels = [1500] * 8  # Initialize RC channels with neutral PWM values
        self.ui_inputs = [0] * 8  # Placeholder for inputs from the UI

    def update_ui_inputs(self, inputs):
        """
        Updates the inputs from the UI.
        """
        if len(inputs) == len(self.ui_inputs):
            self.ui_inputs = inputs
        else:
            raise ValueError("Mismatch in number of UI inputs. Expected 8 inputs.")

    def process_inputs(self):
        """
        Processes inputs from the UI and computes RC channel values.
        """
        print(f"[DEBUG] Raw UI inputs: {self.ui_inputs}")  # Debug print
        self.apply_mixing_logic()
        print(f"[DEBUG] Processed RC channels: {self.rc_channels}")  # Debug print
        self.update_rc_converter()

    def apply_mixing_logic(self):
        """
        Maps UI inputs to RC channel values and applies additional processing logic.
        """
        # Direct mapping for testing
        for i in range(8):
            if self.ui_inputs[i] == 1:
                self.rc_channels[i] = 2000
            elif self.ui_inputs[i] == 0:
                self.rc_channels[i] = 1000

        # Ensure RC channel values are within valid bounds
        for i in range(len(self.rc_channels)):
            if self.rc_channels[i] > 2000:
                self.rc_channels[i] = 2000
            if self.rc_channels[i] < 1000:
                self.rc_channels[i] = 1000

    def update_rc_converter(self):
        """
        Updates the RC converter with the computed RC channel values.
        """
        self.rc_converter.update_channels(self.rc_channels)

    def get_rc_channels(self):
        """
        Returns the computed RC channel values.
        """
        return self.rc_converter.get_channels()

    def get_rc_channels_display(self):
        """
        Returns a string representation of the RC channel values.
        """
        return self.rc_converter.get_channels_display()
