#include <Arduino.h>

#define MOSFET_PIN 3

void setup()
{
  Serial.begin(115200);
  pinMode(MOSFET_PIN, OUTPUT);
}

void loop()
{
  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ON")
    {
      analogWrite(MOSFET_PIN, 255);
      Serial.println("Motor ON");
    }
    else if (cmd == "OFF")
    {
      analogWrite(MOSFET_PIN, 0);
      Serial.println("Motor OFF");
    }
  }
}
