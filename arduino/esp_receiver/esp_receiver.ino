#include <IRremoteESP8266.h>
#include <IRremoteInt.h>
#include <ESP8266WiFi.h>

// Wifi 
WiFiClient client;
IPAddress server(192, 168, 1, 40);
char ssid[] = "ssid";     // the name of your network
char pass[] = "pass";
int status = WL_IDLE_STATUS;     // the Wifi radio's status

// Receiving and decoding IR signals
int RECV_PIN = 2; //an IR detector/demodulatord is connected to GPIO pin 2
IRrecv irrecv(RECV_PIN);
decode_results results;

//Id of the esp
String myId = "espreceiver";
//Ip and port of the server
String serverAddr = "192.168.1.40:3000";

void setup()
{
  Serial.begin(9600);
  
  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }
  
 // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) { 
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:    
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }
  
  // you're connected now, so print out the data:
  Serial.print("You're connected to the network");
  irrecv.enableIRIn(); // Start the receiver
}


void dump(decode_results *results) {
  // Dumps out the decode_results structure.
  // Call this after IRrecv::decode()
  int count = results->rawlen;
  if (results->decode_type == UNKNOWN) {
    Serial.print("Unknown encoding: ");
  }
  else if (results->decode_type == NEC) {
    Serial.print("Decoded NEC: ");

  }
  else if (results->decode_type == SONY) {
    Serial.print("Decoded SONY: ");
  }
  else if (results->decode_type == RC5) {
    Serial.print("Decoded RC5: ");
  }
  else if (results->decode_type == RC6) {
    Serial.print("Decoded RC6: ");
  }
  else if (results->decode_type == PANASONIC) {
    Serial.print("Decoded PANASONIC - Address: ");
    Serial.print(results->panasonicAddress, HEX);
    Serial.print(" Value: ");
  }
  else if (results->decode_type == LG) {
    Serial.print("Decoded LG: ");
  }
  else if (results->decode_type == JVC) {
    Serial.print("Decoded JVC: ");
  }
  else if (results->decode_type == AIWA_RC_T501) {
    Serial.print("Decoded AIWA RC T501: ");
  }
  else if (results->decode_type == WHYNTER) {
    Serial.print("Decoded Whynter: ");
  }
  Serial.print(results->value, HEX);
  Serial.print(" (");
  Serial.print(results->bits, DEC);
  Serial.println(" bits)");
  Serial.print("Raw (");
  Serial.print(count, DEC);
  Serial.print("): ");

  for (int i = 1; i < count; i++) {
    if (i & 1) {
      Serial.print(results->rawbuf[i]*USECPERTICK, DEC);
    }
    else {
      Serial.write('-');
      Serial.print((unsigned long) results->rawbuf[i]*USECPERTICK, DEC);
    }
    Serial.print(" ");
  }
  Serial.println();
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    dump(&results);

    // Sends a message to the server
    if (client.connect(server, 3000)) {
      String hisId = "espsender";
      // Make a HTTP request:
      String url = "/event?ownId=" + myId + "&otherId=" + hisId;
      client.println("POST " + url + " HTTP/1.1");
      //client.println("POST /event?ownId=1&otherId=2 HTTP/1.1");
      client.println("Host: " + serverAddr);
      client.println("Connection: close");
      client.println();

      Serial.println("HTTP POST " + url + " to " + serverAddr);
    }
    irrecv.resume(); // Receive the next value
  }
}
