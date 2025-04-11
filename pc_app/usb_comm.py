import serial
import time
import serial.tools.list_ports

class USBComm:
    def __init__(self, port, baudrate=115200):
        """
        Initializes the USB communication with the ESP device.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def connect(self, retries=3, delay=2):
        """
        Establishes a connection to the ESP device with retries.
        """
        for attempt in range(retries):
            try:
                self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
                time.sleep(2)  # Wait for the connection to stabilize
                print(f"[INFO] Connected to ESP on {self.port} at {self.baudrate} baud.")
                return
            except serial.SerialException as e:
                print(f"[ERROR] Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)

        print("[ERROR] All connection attempts failed. Please check the port and try again.")

    def send_rc_channels(self, channels):
        """
        Sends RC channel values to the ESP device.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            print("[ERROR] Serial connection is not open.")
            return

        try:
            # Format and send data
            data = ",".join(map(str, channels)) + "\n"
            self.serial_connection.write(data.encode('utf-8'))
            self.serial_connection.flush()  # Ensure all data is sent
            print(f"[DEBUG] Sent to Arduino: {data.strip()}")

            # Try to read response
            if self.serial_connection.in_waiting:
                response = self.serial_connection.readline().decode('utf-8').strip()
                print(f"[DEBUG] Arduino response: {response}")
        except Exception as e:
            print(f"[ERROR] Failed to send RC channels: {e}")

    def disconnect(self):
        """
        Closes the connection to the ESP device.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("[INFO] Disconnected from ESP.")

    @staticmethod
    def detect_arduino():
        """
        Detects if an Arduino is connected by checking available serial ports.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description or "CH340" in port.description:
                print(f"[INFO] Arduino detected on {port.device} ({port.description}).")
                return port.device
        print("[INFO] No Arduino detected.")
        return None
