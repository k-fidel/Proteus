#include <Wire.h>
#define up  7
#define down  6


void setup() {
  Wire.begin(7);
  pinMode(up,INPUT);
  pinMode(down,INPUT);
  Wire.onRequest(requestEvent);
}

void loop() {
  delay(100);
}



void requestEvent(){
  if (digitalRead(up)){
    Wire.write("U");
  }
  if (digitalRead(down)){
    Wire.write("D");
  }
}
