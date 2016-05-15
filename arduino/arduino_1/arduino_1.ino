#include <TimerOne.h>
#include <IRLib.h>

//Create a receiver object to listen on pin 8
IRrecv My_Receiver(8);

IRsend My_Sender(4);

//Create a decoder object
IRdecode My_Decoder;

void setup()
{
  Serial.begin(9600);
  Serial.print("ARDUINO 1 \n");
  
  Timer1.initialize(1200000); // 0.1 s
  Timer1.pwm(9,512);
  Timer1.attachInterrupt(callback); 
  
}

void callback(){
   My_Sender.send(SONY,0x1234, 20);
  My_Receiver.enableIRIn();
  Serial.print("Message envoyé ! \n");
}

void loop() {
  if (My_Receiver.GetResults(&My_Decoder)) {
    My_Decoder.decode();
    My_Decoder.DumpResults();
    My_Receiver.resume();     //Restart the receiver
  }

}
