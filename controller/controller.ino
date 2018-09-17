#include <FastLED.h>

#define NUM_LEDS_A 129
#define NUM_LEDS_B 129

#define DATA_PIN_A 2
#define DATA_PIN_B 8

#define OFFSET_A 121
#define OFFSET_B 121

#define SERIALRATE 500000

#define CALIBRATION_TEMPERATURE TypicalLEDStrip  // Color correction
#define GLOBAL_BRIGHTNESS 255 // 0-255

const uint8_t prefix_a = 'A';
const uint8_t prefix_b = 'B';

const int offset_a_bytes = 3 * OFFSET_A;
const int offset_b_bytes = 3 * OFFSET_B;
const int leds_a_bytes = 3 * NUM_LEDS_A;
const int leds_b_bytes = 3 * NUM_LEDS_B;

CLEDController *ctl_a;
CLEDController *ctl_b;

const int readbuf_size = max(leds_a_bytes, leds_b_bytes);
char readbuf[readbuf_size];

CRGB leds_a[NUM_LEDS_A];
CRGB leds_b[NUM_LEDS_B];

void setup()
{

  ctl_a = &FastLED.addLeds<WS2811, DATA_PIN_A, GRB>(leds_a, NUM_LEDS_A);
  ctl_b = &FastLED.addLeds<WS2811, DATA_PIN_B, GRB>(leds_b, NUM_LEDS_B);
  //ctl_a = &FastLED.addLeds<NEOPIXEL, DATA_PIN_A>(leds_a, NUM_LEDS_A);
  //ctl_b = &FastLED.addLeds<NEOPIXEL, DATA_PIN_B>(leds_b, NUM_LEDS_B);

  ctl_a->setTemperature(CALIBRATION_TEMPERATURE);
  ctl_b->setTemperature(CALIBRATION_TEMPERATURE);

  for(int i = 0; i < NUM_LEDS_A; i++) {
    leds_a[i] = CRGB(255, 68, 0); // orangey
  }
  for(int i = 0; i < NUM_LEDS_B; i++) {
    leds_b[i] = CRGB(0, 120, 210); // bluey
  }

  ctl_a->showLeds(GLOBAL_BRIGHTNESS);
  ctl_b->showLeds(GLOBAL_BRIGHTNESS);

  Serial.begin(SERIALRATE);
}

void loop() {
  while (!Serial.available());

  uint8_t in = Serial.read();
  if (in == prefix_a) {

    Serial.readBytes((char*)readbuf, leds_a_bytes);
    memcpy((char*)leds_a + offset_a_bytes, (char*)readbuf, leds_a_bytes - offset_a_bytes);
    memcpy((char*)leds_a, (char*)readbuf + leds_a_bytes - offset_a_bytes, offset_a_bytes);

    ctl_a->showLeds(GLOBAL_BRIGHTNESS);

  } else if (in == prefix_b) {

    Serial.readBytes((char*)readbuf, leds_b_bytes);
    memcpy((char*)leds_b + offset_b_bytes, (char*)readbuf, leds_b_bytes - offset_b_bytes);
    memcpy((char*)leds_b, (char*)readbuf + leds_b_bytes - offset_b_bytes, offset_b_bytes);

    ctl_b->showLeds(GLOBAL_BRIGHTNESS);

  }
}
