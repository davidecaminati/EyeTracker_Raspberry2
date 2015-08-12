// Bounce.pde
// -*- mode: C++ -*-
//
// Make a single stepper bounce from one limit to another
//
// Copyright (C) 2012 Mike McCauley
// $Id: Random.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

/*
 FUNCTION = 0, DRIVER = 1, FULL2WIRE = 2, FULL3WIRE = 3,
  FULL4WIRE = 4, HALF3WIRE = 6, HALF4WIRE = 8 
*/
#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(8,4,5,6,7); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

volatile boolean Allarme = false;

int pin_velocita = A0;
int pin_ampiezza = A1;
int pin_accelerazione = A2;
int maxSpeed = 500;
int acceleration = 300;
int ampiezza = 0;
int old_val_ampiezza = 0;


int val_velocita;
int val_ampiezza;
int val_accelerazione;

boolean stringComplete = false;  // whether the string is complete
String inputString = "";         // a string to hold incoming data

boolean Debug = true;
void setup()
{  
  // Change these to suit your stepper if you want
  stepper.setMaxSpeed(maxSpeed);
  stepper.setAcceleration(acceleration);
  stepper.move(ampiezza);
  
  // trimmers
  pinMode(pin_velocita,INPUT_PULLUP);
  pinMode(pin_accelerazione,INPUT_PULLUP);
  pinMode(pin_ampiezza,INPUT_PULLUP);
  
  //
  
  /*
  pinMode(2,INPUT_PULLUP);
  pinMode(3,INPUT_PULLUP);
  attachInterrupt(0, AllarmeHandler, FALLING); // pin 2
  attachInterrupt(1, RiarmaHandler, FALLING); // pin 3
  
  */
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  
  // Serial
  
    // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop()
{
    if (Debug) {
      val_velocita = 700;
      val_ampiezza = 4000;
      val_accelerazione = 200;
    }
    else
    {
      val_velocita = analogRead(pin_velocita);
      val_ampiezza = analogRead(pin_ampiezza) * 10 ;
      val_accelerazione = analogRead(pin_accelerazione) /6 ;
    }
    
    stepper.setMaxSpeed(val_velocita);
    
    if (abs(old_val_ampiezza - val_ampiezza) > 100){
      old_val_ampiezza = val_ampiezza;
      ampiezza = val_ampiezza;
    }
    
    stepper.setAcceleration(val_accelerazione);
    
    
    if (Allarme){
        stepper.disableOutputs();
        StopMotore();
        stepper.setCurrentPosition(0);
    }
    else
    {
        stepper.enableOutputs();
        //StartMotore();
        //stepper.moveTo(150000);
        Muovi();
    }
    
    
    if (stringComplete) {
      Serial.println(inputString);
      if (inputString.startsWith("--L")) 
      {
        StartMotore();
        stepper.move(ampiezza); 
      };
      if (inputString.startsWith("--R"))
      {
        StartMotore();
        stepper.move(-ampiezza);
      }
      if (inputString.startsWith("--A"))  // allarme
      {
        stepper.disableOutputs();
        StopMotore();
        stepper.move(0);
      }
      if (inputString.startsWith("--D"))   // disarma
      {
        stepper.enableOutputs();
        stepper.move(0);
      }
  
      // clear the string:
      inputString = "";
      stringComplete = false;
  }
    
}

void AllarmeHandler(){
  Allarme = true;
}

void RiarmaHandler(){
  Allarme = false;
}


void Muovi(){
      // If at the end of travel go to the other end
    if (stepper.distanceToGo() == 0){
      stepper.disableOutputs();
      StopMotore();
      //delay(500);
      //stepper.moveTo(-stepper.currentPosition());
    }
    //stepper.run();
    stepper.run();
    
}

void StopMotore(){
    digitalWrite(8,true);
    digitalWrite(9,true);
}
void StartMotore(){
    digitalWrite(8,false);
    digitalWrite(9,false);
}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
