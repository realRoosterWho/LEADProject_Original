#include <WiFi.h>//在线
const char *wifi_name= "RW";//不能改的变量
const char *wifi_password = "23333333";

#include <PubSubClient.h>
WiFiClient wifi_client;

int vibration_pin1 = 1;
int vibration_pin2 = 2;
int vibration_pin3 = 3;
int vibration_pin4 = 4;
int vibration_pin5 = 5;

int value1 = 0;
int value2 = 0;
int value3 = 0;
int value4 = 0;
int value5 = 0;

int status1 = 0;
int status2 = 0;
int status3 = 0;
int status4 = 0;
int status5 = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  wifi_connect_func(wifi_name, wifi_password);

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

    int value4 = Serial.parseInt();
    Serial.readStringUntil(',');
    status4 = value4;
    analogWrite(vibration_pin4, status4);
    Serial.print("status4 of vibration: ");
    Serial.println(status4);

    int value3 = Serial.parseInt();
    Serial.readStringUntil(',');
    status3 = value3;
    analogWrite(vibration_pin3, status3);
    Serial.print("status3 of vibration: ");
    Serial.println(status3);

    int value1 = Serial.parseInt();
    Serial.readStringUntil(',');
    status1 = value1;
    analogWrite(vibration_pin1, status1);
    Serial.print("status1 of vibration: ");
    Serial.println(status1);

    int value5 = Serial.parseInt();
    Serial.readStringUntil(',');
    status5 = value5;
    analogWrite(vibration_pin5, status5);
    Serial.print("status5 of vibration: ");
    Serial.println(status5);
    
    int value2 = Serial.parseInt();
    Serial.readStringUntil(',');
    status2 = value2;
    analogWrite(vibration_pin2, status2);
    Serial.print("status2 of vibration: ");
    Serial.println(status2);



  }
}

void wifi_connect_func(const char *ssid, const char *pw)
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pw);
  Serial.println("");
  Serial.print("[WIFI] Connecting to: ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("[WIFI] Connected!");
  Serial.print("[WIFI] IP is: ");
  Serial.println(WiFi.localIP());

}
