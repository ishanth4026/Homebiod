#include <Arduino.h>


void setup() {
    Serial.begin(115200);
    delay(10000); // Wait for Serial to initialize
    Serial.println("READY");
}

void loop() {
    if (Serial.available()>0) {
        String message = Serial.readStringUntil('\n');
        message.trim(); // Remove any leading/trailing whitespace
        int colonIndex = message.indexOf(':');
        if (colonIndex == -1) {
            if (message == "PING"){
                Serial.println("PONG");
            } else {
                Serial.println("Unknown command");
            }
        } else {
            String command = message.substring(0, colonIndex);
            String value = message.substring(colonIndex + 1);
            command.trim();
            if (command == "PRINT") {
                Serial.println(value);
            } else {
                Serial.println("Unknown command");
            }
        }

    }

}
