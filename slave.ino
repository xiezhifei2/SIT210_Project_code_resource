#include <Wire.h>

const int led = D7; 
int feed = D6;

void setup() {
    
    Wire.begin(0x9);
    
    pinMode(led, OUTPUT);
    pinMode(feed, OUTPUT);
    digitalWrite(led, LOW);
    digitalWrite(feed, LOW);
    
    
    Particle.function("feed",feedToggle);
    
    Wire.onReceive(receiveEvent);
}



void receiveEvent(int byteCount) {
    while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a number
    digitalWrite(led, c);
  }
}
  
void loop() {
    if(digitalRead(led) == HIGH){
        Particle.publish("status", "less_food", PUBLIC);
    }
    delay(2s);
}

int feedToggle(String command) {
    if (command=="feed") {
        digitalWrite(feed,HIGH);
        delay(5s);
        digitalWrite(feed,LOW);
        return 1;
    }
}