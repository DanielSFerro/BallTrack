/* Esteira_movimento.ino
* Versão 0.3
*
* Código para movimentar a esteira da Autobotz, utilizando o HAMS, a partir
* de comandos enviados por um nó do ROS que contem o algoritmo de decisão
* de movimento.
*
* v_0.3: Pacote rosserial_arduino substituido pela biblioteca rs232.h
* __________________________________________________________________________
*/
#include "Buzzer_R2D2.h"
#define motor_esq_DIR 5
#define motor_esq_PWM 6
#define motor_dir_DIR 9
#define motor_dir_PWM 10
#define largura 50 // Distância entre as rodas (esteiras) em cm
#define velpwm_conv 7.7 // Constante de conversão de cm/s para PWM
int indicadorBuzzer = 0;
int flagAtual=0;
int flagAntigo=1;

void Mover(int vel_pwm, int dir, int PWM)
{
  if(vel_pwm > 255)
    vel_pwm = 255;
  else if(vel_pwm < -255)
    vel_pwm = -255;
    
  if (PWM == motor_dir_PWM)
    Serial.print("Direita = ");
  else if (PWM == motor_esq_PWM)
    Serial.print("Esquerda = ");
  else
    Serial.print("What the fuck = ");

  Serial.print(vel_pwm);
  Serial.println("--//--");
  
  if(vel_pwm < 0)
    digitalWrite(dir,HIGH);
  else
    digitalWrite(dir,LOW);
  
  analogWrite(PWM,abs(vel_pwm));
}

float vel_linear = 0, vel_angular = 0;
int pwm_esq = 0, pwm_dir = 0, flag = 0;
int i;
char comando[20];
boolean stringCompleta = false;

// ___________________________________________________________________________
void setup()
{
  Serial.begin(9600);
  pinMode(motor_esq_PWM,OUTPUT);
  pinMode(motor_esq_DIR,OUTPUT);
  pinMode(motor_dir_PWM,OUTPUT);
  pinMode(motor_dir_DIR,OUTPUT);
  pinMode(13, OUTPUT);
}
void loop()
{
  if (stringCompleta)
  {
    stringCompleta = false;
    float vel_diferencial = vel_angular * largura;
    pwm_esq = velpwm_conv * (vel_linear + vel_diferencial/2);
    pwm_dir = velpwm_conv * (vel_linear - vel_diferencial/2);
 
    Serial.print("L = ");
    Serial.print(vel_linear);
    Serial.print(", A = ");
    Serial.print(vel_angular);
    Serial.print(", F = ");
    Serial.print(flag);
    Serial.print(", D = ");
    Serial.print(vel_diferencial);
    Serial.print(", esq = ");
    Serial.print(pwm_esq);
    Serial.print(", dir = ");
    Serial.print(pwm_dir);
    Serial.println("--//--");

    switch(flag){
      case 0:                         // Movimento normal
        Mover(pwm_esq, motor_esq_DIR, motor_esq_PWM);
        Mover(pwm_dir, motor_dir_DIR, motor_dir_PWM);
        if(indicadorBuzzer==0) r2D2();
        indicadorBuzzer=1;
        flagAntigo=0;
        break;
    
      case -1:                        // Giro em torno do próprio eixo (esquerda)
        
        Mover(-100, motor_esq_DIR, motor_esq_PWM);
        Mover(100, motor_dir_DIR, motor_dir_PWM);
        if(indicadorBuzzer==0) catcall();
        indicadorBuzzer=1;
        flagAntigo=-1;
        break;
      
      case 1:                         // Giro em torno do próprio eixo (direita)
        
        Mover(100, motor_esq_DIR, motor_esq_PWM);
        Mover(-100, motor_dir_DIR, motor_dir_PWM);
        if(indicadorBuzzer==0) waka();
        indicadorBuzzer=1;
        flagAntigo=1;
        break;
      
      default:                        // Esteira parada
        Mover(0, motor_esq_DIR, motor_esq_PWM);
        Mover(0, motor_dir_DIR, motor_dir_PWM);
        if(indicadorBuzzer==0) uhoh();
        indicadorBuzzer=1;
        flagAntigo=2;
        break;
    }
  }
  delay(5);
}

void serialEvent()
{
  if(Serial.available())
  {
    comando[i] = Serial.read();
    if (comando[i++] == '\n')
    {
      while(Serial.available())
        Serial.read();
    
      i = 0;
      vel_linear = atof(strtok(comando,","));
      vel_angular = atof(strtok(NULL,","));
      flag = atoi(strtok(NULL,","));
      stringCompleta = true;
      
      switch(flag){
        case 0:       
          flagAtual=0;
        break;
        case -1:                        
           flagAtual=-1;
        break;
        case 1:                         
            flagAtual=1;
        break;
        default:                      
            flagAtual=2; 
        break;
      }
      if(flagAtual!=flagAntigo) indicadorBuzzer=0;
    }
  }
}
