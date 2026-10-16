#include <Arduino.h>
#include <SPI.h>
#include "utilities.h"     
#include <GxEPD2_BW.h>
#include <Adafruit_GFX.h>



GxEPD2_BW<GxEPD2_213_BN, GxEPD2_213_BN::HEIGHT> display(
    GxEPD2_213_BN(EDP_CS_PIN, EDP_DC_PIN, EDP_RSET_PIN, EDP_BUSY_PIN)
);

void setup() {
    Serial.begin(115200);
    SPI.begin(EDP_CLK_PIN, EDP_MISO_PIN, EDP_MOSI_PIN, EDP_CS_PIN);
    display.init(115200, true, 50, false); 
    display.setRotation(1);
    delay(1000);
    
    Serial.println("Display initialized and cleared.");
 


    display.firstPage();
    do {
        display.fillScreen(GxEPD_WHITE);
        display.setTextColor(GxEPD_BLACK);
        display.setTextSize(2);
        display.drawRect(0,0,250,122,GxEPD_BLACK);
        display.drawFastHLine(0,35,250,GxEPD_BLACK);
        display.setCursor(15, 10);
        display.print("Text");

        display.setTextSize(1);
        display.setCursor(15, 55);
        display.print("Status Ready");
    } while (display.nextPage());
}

void loop(){
    Serial.println("Display initialized and cleared.");
}