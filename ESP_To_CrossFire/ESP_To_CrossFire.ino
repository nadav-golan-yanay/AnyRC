#define PPM_PIN 12
#define CHANNELS 8
#define PPM_PULSE_LENGTH 300
#define PPM_FRAME_LENGTH 22500

int rcChannels[CHANNELS] = {1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};
String inputBuffer = "";

void setup() {
  Serial.begin(115200);
  pinMode(PPM_PIN, OUTPUT);
  digitalWrite(PPM_PIN, LOW);

  // Optional: startup message
  Serial.println("[ESP32] Ready for RC data over USB");
}

void loop() {
  // --- Handle serial input ---
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      parseChannels(inputBuffer);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }

  // --- Generate one PPM frame ---
  generatePPMFrame();
}

void parseChannels(const String& data) {
  int index = 0;
  int lastComma = -1;
  String cleaned = data;
  cleaned.trim();

  for (int i = 0; i < cleaned.length(); i++) {
    if (cleaned.charAt(i) == ',' || i == cleaned.length() - 1) {
      int end = (i == cleaned.length() - 1) ? i + 1 : i;
      String valueStr = cleaned.substring(lastComma + 1, end);
      int val = valueStr.toInt();

      if (index < CHANNELS && val >= 900 && val <= 2200) {
        rcChannels[index] = val;
      }

      lastComma = i;
      index++;
    }
  }
}

void generatePPMFrame() {
  unsigned long start = micros();

  for (int i = 0; i < CHANNELS; i++) {
    digitalWrite(PPM_PIN, HIGH);
    delayMicroseconds(PPM_PULSE_LENGTH);

    digitalWrite(PPM_PIN, LOW);
    delayMicroseconds(rcChannels[i] - PPM_PULSE_LENGTH);
  }

  // Sync
  unsigned long used = micros() - start;
  unsigned long sync = PPM_FRAME_LENGTH - used;
  if (sync > PPM_PULSE_LENGTH) {
    digitalWrite(PPM_PIN, HIGH);
    delayMicroseconds(PPM_PULSE_LENGTH);
    digitalWrite(PPM_PIN, LOW);
    delayMicroseconds(sync - PPM_PULSE_LENGTH);
  }
}
