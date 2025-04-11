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
                time.sleep(2)
                return True
            except serial.SerialException:
                time.sleep(delay)
        return False

    def send_rc_channels(self, channels):
        """
        Sends RC channel values to the ESP device.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            return False

        try:
            data = ",".join(map(str, channels)) + "\n"
            self.serial_connection.write(data.encode('utf-8'))
            self.serial_connection.flush()
            return True
        except Exception:
            return False

    def disconnect(self):
        """
        Closes the connection to the ESP device.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()

    @staticmethod
    def detect_arduino():
        """
        Detects if an Arduino is connected by checking available serial ports.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description or "CH340" in port.description:
                return port.device
        return None
