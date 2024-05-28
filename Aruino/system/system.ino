#include <Servo.h>
#include <string.h>

Servo servo1;
Servo servo2;
void setup(){
  servo1.attach(9);
  servo2.attach(10);
  servo1.write(90);
  servo2.write(90);
  Serial.begin(9600);
  Serial.setTimeout(100);
}
int phi1 = 90;
int phi2 = 90;
String command = "";
void loop(){
  if (Serial.available() > 0){
    command = Serial.readString();
    long i = command.toInt();
    phi1 = i / 1000;
    phi2 = i % 1000;
    String retu = String(phi1) + '-' + String(phi2) + '\n';
    Serial.print(retu);
  }
  //Serial.write("hi");
  servo1.write(phi1);
  servo2.write(phi2);
  delay(10);
}