#include <NewPing.h>
#define TRIGGER_PIN1  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN1     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define TRIGGER_PIN2  10  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN2     9  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define TRIGGER_PIN3  8  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN3     7  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define TRIGGER_PIN4  6  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN4     5  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200000 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar1(TRIGGER_PIN1, ECHO_PIN1, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar3(TRIGGER_PIN3, ECHO_PIN3, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar4(TRIGGER_PIN4, ECHO_PIN4, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results.
  pinMode(13,OUTPUT);
}

void loop() {
  delay(50);                      // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  unsigned int uS1 = sonar1.ping(); // Send ping, get ping time in microseconds (uS).
  float dist1=(sonar1.convert_cm(uS1)); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
  unsigned int uS2 = sonar2.ping(); // Send ping, get ping time in microseconds (uS).
  float dist2=(sonar2.convert_cm(uS2)); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
  unsigned int uS3 = sonar3.ping(); // Send ping, get ping time in microseconds (uS).
  float dist3 =(sonar3.convert_cm(uS3)); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
  unsigned int uS4 = sonar4.ping(); // Send ping, get ping time in microseconds (uS).
  float dist4=(sonar4.convert_cm(uS4)); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
  Serial.println(dist1);
  Serial.println(dist2);
  Serial.println(dist3);
  Serial.println(dist4);
  Serial.print('\n');
  if(dist1<20||dist2<20||dist3<20||dist4<20)
    if(dist1!=0 && dist2!=0 && dist3!=0 && dist4!=0)
     digitalWrite(13,HIGH); // A LED is going to be on just in case of an object is too close to the robot
  else 
    digitalWrite(13,LOW);
}
