#include "OneWire.h"

OneWire ds(10);
//this means pin 10^
#define LED_IDLE_PERIOD 1000
unsigned long LEDIdleTime;
bool led_is_high=true;
#define LED_PIN BLUE_LED
void setup(void) {
  pinMode(LED_PIN,OUTPUT); //LED
  digitalWrite(LED_PIN,LOW);
  Serial.begin(9600);
  LEDIdleTime = millis() + LED_IDLE_PERIOD;

//the baud value is 9600^
}

void loop() {
  // put your main code here, to run repeatedly: 
  if ((long) (millis() - LEDIdleTime) > 0) {
    LEDIdleTime = millis() + LED_IDLE_PERIOD;
    switch_LED();
  }
  delay(1000);
  // bytes mean variable types
  byte arraynumber;
  byte resetcheck;
  byte chipnumber;
  byte data[12];
  byte addr[8];
  float celsius, fahrenheit;



  if ( !ds.search(addr)){
    //Serial.println("  No more addresss.");
    //Serial.println();
    ds.reset_search();
    delay(250);
    return;
  }

  switch (addr[0]) {
    case 0x10:
      //Serial.println(" ");
      //Serial.println("Tempeature Sensor = DS18S20:");  // or old DS1820
      chipnumber = 1;
      break;
    case 0x28:
      //Serial.println(" ");
      //Serial.println("Temperature Sensor = DS18B20:");
      chipnumber = 0;
      break;
    case 0x22:
      //Serial.println(" ");
      //Serial.println("Temperature Sensor = DS1822:");
      chipnumber = 0;
      break;
    default:
      //Serial.println(" ");
      //Serial.println("Device is not a DS18x20 family device:");
      return;
  }
  
  //Serial.println(" ");
  //Serial.print("  Chip Number =");
  
  for( arraynumber = 0; arraynumber < 8; arraynumber++) {
  Serial.write(' ');
  Serial.print(addr[arraynumber], HEX);
  }
   
  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1); 
  
  delay(1000);

  resetcheck = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);

  //Serial.print("  Data = ");
  //Serial.print(resetcheck, HEX);
  //Serial.print(" ");
  for ( arraynumber = 0; arraynumber < 9; arraynumber++) {
  data[arraynumber] = ds.read();
  //Serial.print(data[arraynumber], HEX);
  //Serial.print(" ");
  }
 int16_t raw = (data[1] << 8) | data[0];
  if (chipnumber){
    raw = raw << 3;
    if (data[7] == 0x10) {
      raw = (raw & 0xFFF0) + 12 - data[6];
      }
  }
    else {
   byte cfg = (data[4] & 0x60);
    if (cfg == 0x00) raw = raw & ~7;
    else if (cfg == 0x20) raw = raw & ~3; 
    else if (cfg == 0x40) raw = raw & ~1; 
}
  celsius = (float)raw / 16.0;
  fahrenheit = celsius * 1.8 + 32.0;
//  Serial.println();
//  Serial.print("   Celsius = ");
  Serial.print(" ");
  Serial.println(celsius);
//  Serial.print("   Fahrenheit = ");
//  Serial.println(fahrenheit); 

  if (OneWire::crc8(addr, 7) != addr[7]) {
  //Serial.println(" ");
  //Serial.println("  CRC is not valid!");
  return;
  }
  
 else {
   OneWire::crc8(data, 8);
   //Serial.println();
   //Serial.print("  CRC = ");
   //Serial.print(, HEX);
   //Serial.println();
 }
}

void switch_LED(){
  if(led_is_high){
    led_is_high=false;
    digitalWrite(LED_PIN,LOW);
  }
  else{    
    led_is_high=true;
    digitalWrite(LED_PIN,HIGH);
  }
}
