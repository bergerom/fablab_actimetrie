#include <IRremoteESP8266.h>
#include <IRremoteInt.h>

#include <ESP8266WiFi.h>
#include <WiFiClient.h>

char ssid[] = "vostro38";     // the name of your network
char pass[] = "dEg0DVAF";
int status = WL_IDLE_STATUS;     // the Wifi radio's status

IRsend irsend(14); //an IR led is connected to GPIO pin 0

void setup()
{

  Serial.begin(9600);

  Serial.println("Attempting to connect to open network...");
  status = WiFi.begin(ssid,pass);
  // if you're not connected, stop here:
  if ( status != WL_CONNECTED) { 
    Serial.println("Couldn't get a wifi connection");
    while(true);
  } 
  // if you are connected :
  else {
      Serial.print("Connected to the network");
  }
  irsend.begin();
}

void loop() {
  Serial.println("NEC");
  irsend.sendNEC(0x00FFE01F, 36);
  delay(2000);
  Serial.println("Sony");
  irsend.sendSony(0xa90, 12);
  delay(2000);
}
