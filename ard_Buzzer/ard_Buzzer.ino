#include "Buzzer_R2D2.h"
void setup() {
   
  // put your setup code here, to run once:
  pinMode(12,INPUT); // Pino que vem de outro arduino
  pinMode(11,INPUT); // Pino que vem de outro arduino
  pinMode(13,OUTPUT); // Buzzer
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(12) == HIGH and digitalRead(11)==LOW) // bolinha está muito a esquerda?
    r2D2(); // Toca musica
  else if(digitalRead(12)==LOW and digitalRead(11)==HIGH) // bolinha está muito a direita?
    squeak(); //Toca musica
}
