#include <UTFT.h>
#include <UTouch.h>

// Declare which fonts we will be using
//extern uint8_t SmallFont[];
extern uint8_t arial_bold[];

// Uncomment the next line for Arduino 2009/Uno
//UTFT(byte model, int RS, int WR,int CS, int RST,int ALE,int SER)
//UTFT myGLCD(ITDB32S,A1,A2,A0,A4,A5);    // Remember to change the model parameter to suit your display module!

// Uncomment the next line for Arduino Mega
UTFT myGLCD(ITDB32S,38,39,40,41);   // Remember to change the model parameter to suit your display module!

UTouch  myTouch( 6, 5, 4, 3, 2);

int x, y;
char stCurrent[20]="";
int stCurrentLen=0;
char stLast[20]="";
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String LastTesto = "";  // need this as buffer for delete old text in log textbox

String ProjectName = "Progetto MC1   0.8";
int actualpage = -1;

void setup()
{
  
    // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  
  myTouch.InitTouch();
  myTouch.setPrecision(PREC_MEDIUM);
  
// Setup the LCD
  myGLCD.InitLCD();
  myGLCD.setFont(arial_bold);
// Clear the screen and draw the frame
  GoToPage(0);
}

void GoToPage(int number){
  if (number == actualpage) return;
  
  if (number > 2) {
    actualpage = 0;
    number = 0;
    }
    
  if (number == 0){
    actualpage = 0;
    // Clear the screen and draw the frame
    myGLCD.clrScr();
    // static part
    myGLCD.setColor(255, 0, 0);
    myGLCD.fillRect(0, 0, 319, 16);
    myGLCD.setColor(64, 64, 64);
    myGLCD.fillRect(0, 226, 319, 239);
    myGLCD.setColor(255, 255, 255);
    myGLCD.setBackColor(255, 0, 0);
    myGLCD.print(ProjectName, CENTER, 1);
    myGLCD.setBackColor(64, 64, 64);
  
    myGLCD.setColor(0, 0, 255);
    myGLCD.drawRect(0, 17, 319, 225);
    myGLCD.setColor(255, 255, 255); // white font color
    
    myGLCD.setBackColor(0, 0, 0); // black forecolor
    
    // control part
    drawButtons();
    
    //log part
    drawFases(5);
    }
    
    if (number == 1){
    actualpage = 1;
    // Clear the screen and draw the frame
    myGLCD.clrScr();  
    myGLCD.fillScr(0,255,0);
    drawButtons();
    }
    
    if (number == 2){
      
    actualpage = 2;
    // Clear the screen and draw the frame  
    myGLCD.fillScr(255,0,0);
    //myGLCD.clrScr();  
    drawButtons();
    }
    
   
  }

void loop()
{

    if (myTouch.dataAvailable())
    {
      myTouch.read();
      x=myTouch.getX();
      y=myTouch.getY();
      
      if ((y>=130) && (y<=180))  // Upper row
      {
        if ((x>=10) && (x<=150))  // Button: Home
        {
          waitForIt(10, 130, 150, 180);
          GoToPage(0);
        }
        if ((x>=160) && (x<=300))  // Button: Next
        {
          waitForIt(160, 130, 300, 180);
          GoToPage(actualpage+1);
        }
      }
      else
      {
        drawLOG("Test");
        }
    }
    
    if (stringComplete) {
      Serial.println(inputString);
      if (inputString.startsWith("--0")) GoToPage(0);
      if (inputString.startsWith("--1")) GoToPage(1);
      if (inputString.startsWith("--2")) GoToPage(2);


       drawLOG(inputString);
  
      // clear the string:
      inputString = "";
      stringComplete = false;
  }
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


// Draw a red frame while a button is touched
void waitForIt(int x1, int y1, int x2, int y2)
{
  myGLCD.setColor(255, 0, 0);
  for(int i=0;i<10;i++){
    myGLCD.drawRoundRect (x1-i, y1-i, x2+i, y2+i);
  }
  
  while (myTouch.dataAvailable())
    myTouch.read();
    
  myGLCD.setColor(0, 0, 0);
  for(int i=0;i<10;i++){
    myGLCD.drawRoundRect (x1-i, y1-i, x2+i, y2+i);
  }
    
  myGLCD.setColor(255, 255, 255);
  myGLCD.drawRoundRect (x1, y1, x2, y2);
}

void drawFases(int fase_num){
  myGLCD.setFont(arial_bold);

  for (int i=0; i<fase_num; i++)
  {
    String actual_fase = "Fase " + String(i+1);
    myGLCD.print(actual_fase, CENTER, 20+ i*20);
  }
}


void drawButtons()
{
// Draw the two buttons
  myGLCD.setColor(0, 0, 255);
  myGLCD.fillRoundRect (10, 130, 150, 180);
  myGLCD.setColor(255, 255, 255);
  myGLCD.drawRoundRect (10, 130, 150, 180);
  myGLCD.print("Home", 50, 147);
  myGLCD.setColor(0, 0, 255);
  myGLCD.fillRoundRect (160, 130, 300, 180);
  myGLCD.setColor(255, 255, 255);
  myGLCD.drawRoundRect (160, 130, 300, 180);
  myGLCD.print("Next", 195, 147);
  myGLCD.setBackColor (0, 0, 0);

}



void drawLOG(String testo){
  //overwrite old text with same text but black
  myGLCD.setColor(0, 0, 0);        // black
  myGLCD.print(LastTesto, CENTER, 200);
  
  myGLCD.setBackColor(0, 0, 0);    // black forecolor
  myGLCD.setColor(255, 255, 255);  // white
  myGLCD.print(testo, CENTER, 200);
  LastTesto = testo;
}

