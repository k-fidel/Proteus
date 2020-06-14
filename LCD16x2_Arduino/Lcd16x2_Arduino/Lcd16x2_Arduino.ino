#include <LiquidCrystal.h>

LiquidCrystal lcd = LiquidCrystal(2, 3, 4, 5, 6, 7);


void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  lcd.setCursor(2,0);
  lcd.print("Hello World");
  lcd.setCursor(2,1);
  lcd.print("By Nemo");
}
