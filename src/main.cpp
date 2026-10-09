#include <Arduino.h>

void setup() {
  // This opens a communication channel to your laptop at a speed of 115200 baud
  Serial.begin(115200);
  
  // Give it a second to initialize
  delay(1000); 
  
  Serial.println("Hello Boss! I am alive and ready to work.");
}

void loop() {
  // We will print this every 2 seconds
  Serial.println("Still here...");
  delay(2000);
}