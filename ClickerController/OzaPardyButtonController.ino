int micePort = 12;
int menPort = A0;

int miceButton = 1;
int menButton = 1;

boolean restartFlag = false;

char serialPortInput;

void setup()
{
  Serial.begin(9600);
  pinMode(micePort, INPUT);  // Pin 12 = miceButton
  pinMode(menPort, INPUT);  // Pin A0 = menButton
  pinMode(13, OUTPUT);
//  digitalWrite(micePort, HIGH);
//  digitalWrite(menPort,  HIGH);
//  pinMode(resetPort, INPUT);  // Pin 1 = resetButton
}

void loop()
{
  restartFlag = false;
  // Setup all switch positions to HIGH
  digitalWrite(micePort, HIGH);  // Set miceButton to be HIGH
  digitalWrite(menPort, HIGH);  // Set menButton to be HIGH
  //digitalWrite(resetPort, HIGH); // Set resetButton to be HIGH
  serialPortInput = Serial.read();
  while(serialPortInput != 'L') {
    serialPortInput = Serial.read();
    delay(50);
  }
  serialPortInput = 'A';
  
  digitalWrite(13, LOW);
//  delay(10); 
  while(restartFlag == false) {
    miceButton = digitalRead(micePort);
    menButton = digitalRead(menPort);
    //resetButton = digitalRead(1);
  
    if (miceButton == LOW) {
      Serial.println("Mice");
      while(restartFlag == false) {
        serialPortInput = Serial.read();
        if(serialPortInput == 'C') {
					restartFlag = true;
          serialPortInput = 'A';
          break;
        }
        else if (serialPortInput == 'W') {
          serialPortInput = 'A';
          while(restartFlag == false) {
          //  digitalWrite(menPort, HIGH);  // Set menButton to be HIGH
            menButton = digitalRead(menPort);
            if (menButton == LOW) {
              Serial.println("Men");
              while(1) {
                serialPortInput = Serial.read();
                if(serialPortInput == 'C' || serialPortInput =='W') {
                  serialPortInput = 'A';
                  restartFlag = true;
                  break;
                }
              }// while menButton is low
            }//if menButton is LOW
          }// while for menButton check
        }// if answer was wrong
      }// while for miceButton clicked
    }// if miceButton is LOW
    else if (menButton == LOW) {
      Serial.println("Men");
      while(restartFlag == false) {
        serialPortInput = Serial.read();
        if(serialPortInput == 'C') {
          serialPortInput = 'A';
					restartFlag = true;
          break;
        }
        else if (serialPortInput == 'W') {
          serialPortInput = 'A';
          while(restartFlag == false) {
            digitalWrite(micePort, HIGH);  // Set miceButton to be HIGH
            miceButton = digitalRead(micePort);
            if (miceButton == LOW) {
              Serial.println("Mice");
              while(1) {
                serialPortInput = Serial.read();
                if(serialPortInput == 'C' || serialPortInput == 'W') {
                  serialPortInput = 'A';
                  restartFlag = true;
                  break;
                }
              }
            }//if miceButton is LOW
          }// while for miceButton check
        }// if answer was wrong        
      }// while for menButton clicked
    }// if menButton is LOW
  }// while checking for serial input
}

