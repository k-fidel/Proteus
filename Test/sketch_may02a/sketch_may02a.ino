#include <Wire.h>

void setup() {
  // put your setup code here, to run once:
  Wire.begine(7);
//  Wire.onReceive(reciveEvent);
  Wire.onRequest(requestEvent);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);

}

void requestEvent(){
  
}
