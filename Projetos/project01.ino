// Programa: Comunicacao Serial Arduino com Raspberry Pi
// Autor: Henrique Almeida
// Autor: Gustavo Nunes

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
String msg;
sensors_event_t a, g, temp;

void setup() {
   Serial.begin(9600);

   while(!Serial){
    delay(10);
  }
  if (!mpu.begin()){
    Serial.println("Failed to find MPU6050 chip");
    while(1){
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  delay(100);
}
void loop() {
   
  readSerialPort();
  if(msg!=""){
      mpu.getEvent(&a, &g, &temp);
      sendZ();
  }
  delay(500);
}


void readSerialPort() {
  msg = "";
  if (Serial.available()) {
      delay(10);
      while (Serial.available() > 0) {
          msg += (char)Serial.read();
      }
      Serial.flush();
  }
}
void sendData() {
  //write data
  Serial.println(g.gyro.x);
  Serial.println(g.gyro.y);
  Serial.println(g.gyro.z);
}

void sendZ() {
  //write data
  Serial.println(g.gyro.z);
}
