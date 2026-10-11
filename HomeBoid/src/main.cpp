#include <Arduino.h>
#include <SPI.h>
#include <GxEPD2_BW.h>
#include "utilities.h" 

GxEPD2_BW<GxEPD2_213_BN, GxEPD2_213_BN::HEIGHT> display(GxEPD2_213_BN(EDP_CS_PIN, EDP_DC_PIN, EDP_RSET_PIN, EDP_BUSY_PIN));
uint8_t imageBuffer[3904]; 

bool isConnected = false;
unsigned long lastBeacon = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5000); 
  
  SPI.begin(EDP_CLK_PIN, EDP_MISO_PIN, EDP_MOSI_PIN, EDP_CS_PIN);
  display.init(115200);
  display.setRotation(1);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); 
    
    Serial.println("DEBUG_HEARD:" + command); 
    
    if (command == "DRAW") {
      isConnected = true; // Stop broadcasting the beacon
      Serial.println("DEBUG_STARTING_DOWNLOAD");
      size_t bytesRead = Serial.readBytes(imageBuffer, 3904);
      
      Serial.print("DEBUG_BYTES_CAUGHT:");
      Serial.println(bytesRead);
      
      if (bytesRead == 3904) {
        Serial.println("DEBUG_DRAWING_TO_SCREEN");
        display.setFullWindow();
        display.firstPage();
        do {
          display.fillScreen(GxEPD_WHITE);
          display.drawBitmap(0, 0, imageBuffer, 250, 122, GxEPD_WHITE, GxEPD_BLACK);
        } while (display.nextPage());
        Serial.println("DEBUG_SUCCESS");
      }
    }
  } else if (!isConnected) {
    // THE BEACON: Yell READY every 1 second
    if (millis() - lastBeacon > 1000) {
      Serial.println("READY");
      lastBeacon = millis();
    }
  }
}