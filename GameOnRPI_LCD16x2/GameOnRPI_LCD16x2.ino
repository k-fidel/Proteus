#include <Wire.h>
#define Joy_x A7
#define Joy_y A6
#define Joy_pBt 3
int x,y,z;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(12);
  Wire.onRequest(requestEvent);
  pinMode(Joy_x, INPUT);
  pinMode(Joy_y, INPUT);
  pinMode(Joy_pBt, INPUT); // not needed
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);

}

void requestEvent(){
  x = analogRead(Joy_x);
  y = analogRead(Joy_y);
  z = digitalRead(Joy_pBt);
  delay(100);
  if ((0 <= x && x < 510) || (0 <=y && y < 510)){
    if(0 <= y && y < 510){
      Wire.write("U");
    }
    if (0 <= x && x < 510 ){
      Wire.write("L");
    }
  }
  else if ( 510 <= x && x < 528){
    Wire.write("m");
  }
  else if ((528 <= x && x < 1024) || (520 <= y && y < 1030)){
    if (520 <= y && y < 1030){
      Wire.write("D");
    }
    if (528 <=x && x <1025){
      Wire.write("R");
    }
  }
}
