#include <LiquidCrystal.h>
#include <Wire.h>

LiquidCrystal lcd = LiquidCrystal(2, 3, 4, 5, 6, 7);


void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  Wire.begin(8);
  Wire.onReceive(receiveEvent);
  
}

void loop() {
delay(100);
}

void receiveEvent(int howMany){
  while (1 < Wire.available()){
    char c = Wire.read();
    lcd.setCursor(2,0);
    lcd.print(c);
    delay(100);
  }
  int x = Wire.read();
}
