#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "PPMCom.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDR 0x3C

PPMCom ppm;
String inputBuffer = "";

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(115200);
  ppm.begin();

  // Initialize OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    // Hang if OLED not found
    while (true);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("PPM Ready...");
  display.display();
}

void loop() {
  // Read and parse incoming serial data
  /*while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      ppm.updateChannelsFromString(inputBuffer);
      showChannelsOnOLED();  // <-- Show parsed values on screen
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }*/
  char c = Serial.read();
  if (c == '\n') {
    ppm.updateChannelsFromString(inputBuffer);
    showChannelsOnOLED();  // <-- Show parsed values on screen
    inputBuffer = "";
  } else {
    inputBuffer += c;
  }

  // Generate one full PPM frame per loop
  ppm.generatePPM();
}

void showChannelsOnOLED() {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("RC Channels:");

  for (int i = 0; i < 8; i++) {
    display.print("CH");
    display.print(i);
    display.print(": ");
    display.println(ppm.getChannelValue(i)); // <- getter function
  }

  display.display();
}
