#include <WiFi.h>//在线
#include <string.h>

#include <PubSubClient.h>
WiFiClient wifi_client;

int vibration_pin1 = 1;
int vibration_pin2 = 2;
int vibration_pin3 = 3;
int vibration_pin4 = 4;
int vibration_pin5 = 5;

int status1 = 0;
int status2 = 0;
int status3 = 0;
int status4 = 0;
int status5 = 0;

char pattern1;
char pattern2;
char pattern3;
char pattern4;
char pattern5;

// Define the patterns for the vibration, use only 0, 1, and 2
const char *patternA = "0012200122";
const char *patternB = "0122101221";
const char *patternC = "0122102210";
const char *patternD = "0221102211";
const char *patternE = "1221001221";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);


  pinMode(vibration_pin1, OUTPUT);
  pinMode(vibration_pin2, OUTPUT);
  pinMode(vibration_pin3, OUTPUT);
  pinMode(vibration_pin4, OUTPUT);
  pinMode(vibration_pin5, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
  {
    status1 = Serial.parseInt();
    pattern1 = Serial.read(); // read the pattern
    Serial.readStringUntil(',');
    apply_pattern(vibration_pin1, status1, pattern1);

    status2 = Serial.parseInt();
    pattern2 = Serial.read(); // read the pattern
    Serial.readStringUntil(',');
    apply_pattern(vibration_pin2, status2, pattern2);

    status3 = Serial.parseInt();
    pattern3 = Serial.read(); // read the pattern
    Serial.readStringUntil(',');
    apply_pattern(vibration_pin3, status3, pattern3);

    status4 = Serial.parseInt();
    pattern4 = Serial.read(); // read the pattern
    Serial.readStringUntil(',');
    apply_pattern(vibration_pin4, status4, pattern4);
    
    status5 = Serial.parseInt();
    pattern5 = Serial.read(); // read the pattern
    Serial.readStringUntil(',');
    apply_pattern(vibration_pin5, status5, pattern5);
  }
}


void apply_pattern(int pin, int status, char pattern)
{
  const char *p;
  switch(pattern)
  {
    case 'A': p = patternA; break;
    case 'B': p = patternB; break;
    case 'C': p = patternC; break;
    case 'D': p = patternD; break;
    case 'E': p = patternE; break;
    default: return;
  }

  for(int i = 0; i < 10; i++)
  {
    int intensity = (p[i] - '0') * status / 2; // The max value is 2
    analogWrite(pin, intensity);
    delay(500); // delay for 200ms
  }
}
