#include "PPMCom.h"

PPMCom::PPMCom() {
  // Set default values
  for (int i = 0; i < CHANNELS; i++) {
    ppm_values[i] = 1000;
  }
}

void PPMCom::begin() {
  pinMode(PPM_PIN, OUTPUT);
  digitalWrite(PPM_PIN, LOW);
  disarmA();
}

void PPMCom::generatePPM() {
  unsigned long startFrame = micros();

  for (int ch = 0; ch < CHANNELS; ch++) {
    digitalWrite(PPM_PIN, HIGH);
    delayMicroseconds(PPM_PULSE_LENGTH);

    digitalWrite(PPM_PIN, LOW);
    delayMicroseconds(ppm_values[ch] - PPM_PULSE_LENGTH);
  }

  // Sync pulse
  unsigned long frameUsed = micros() - startFrame;
  unsigned long syncLength = PPM_FRAME_LENGTH - frameUsed;

  if (syncLength > PPM_PULSE_LENGTH) {
    digitalWrite(PPM_PIN, HIGH);
    delayMicroseconds(PPM_PULSE_LENGTH);
    digitalWrite(PPM_PIN, LOW);
    delayMicroseconds(syncLength - PPM_PULSE_LENGTH);
  }
}

void PPMCom::disarmA() {
  for (int i = 0; i < CHANNELS; i++) {
    ppm_values[i] = 1000;
  }
}

void PPMCom::updateChannelsFromString(const String& data) {
  int channelIndex = 0;
  int lastComma = -1;
  String trimmedData = data;
  trimmedData.trim();

  for (int i = 0; i < trimmedData.length(); i++) {
    if (trimmedData.charAt(i) == ',' || i == trimmedData.length() - 1) {
      int endIdx = (i == trimmedData.length() - 1) ? i + 1 : i;
      String valueStr = trimmedData.substring(lastComma + 1, endIdx);
      int val = valueStr.toInt();

      if (channelIndex < CHANNELS && val >= 1000 && val <= 2000) {
        ppm_values[channelIndex] = val;
      }

      lastComma = i;
      channelIndex++;
    }
  }
}

int PPMCom::getChannelValue(int ch) {
  if (ch >= 0 && ch < CHANNELS) {
    return ppm_values[ch];
  }
  return 0;
}
