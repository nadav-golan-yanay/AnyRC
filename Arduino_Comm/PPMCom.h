#ifndef PPMCOM_H
#define PPMCOM_H

#include <Arduino.h>

class PPMCom {
  public:
    PPMCom();               // Constructor
    void begin();           // Initialize GPIO pin and reset values
    void generatePPM();     // Generate one full PPM frame
    void disarmA();         // Reset channels to 1000
    void updateChannelsFromString(const String& data);
    int getChannelValue(int ch);

  private:
    static const int CHANNELS = 8;
    static const int PPM_PIN = 9;
    static const int PPM_PULSE_LENGTH = 300;
    static const int PPM_FRAME_LENGTH = 22500;
    int ppm_values[CHANNELS];
};

#endif
