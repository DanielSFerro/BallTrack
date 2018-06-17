#include "Buzzer_R2D2.h"
void setup() {file:///home/samuel/Desktop/Codigo/BallTrack/ard_bolinha/musical_notes.h
   
  // put your setup code here, to run once:
  pinMode(12,INPUT);
  pinMode(11,INPUT);
  pinMode(13,OUTPUT); //BUZZER
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(12) == HIGH and digitalRead(11)==LOW)
    r2D2();
  else if(digitalRead(12)==LOW and digitalRead(11)==HIGH)
    squeak(); 
}
