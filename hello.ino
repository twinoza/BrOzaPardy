
// 12_21_16 First version.
// The protocol is dirt simple.
// Host sends an "S" 
// Arduino responds with either the button that was pressed (2-14, not including 13), or a 0 to indicate no button pressed.

int down = 0;        // none of the buttons are down
int n;               // to scroll through the buttons

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  for (int pin=2; pin < 13; pin++) { // Pin 1 is used for Tx.  The internal 20K pull up prevents stray capacitance causing false status read
    pinMode(pin, INPUT_PULLUP);
  }
    pinMode(A0, INPUT);  // This is A0 on the board.
    digitalWrite(A0, HIGH); // to enable the pull up on an analog pin  
}

void loop() {  // run over and over again
  down = 0;    // assume no buttons are down
  while (Serial.read() != 'S') {
    delay(50);
  }
  // now check buttons 2 through 12 for the first button that is down
  for (int n=1; n < 13; n++) {
      if (digitalRead(n) == LOW) {
        Serial.println(n);
        down = 1;
        break;
      }
  }
  if ((down == 0) && (digitalRead(14) == LOW)) {  // if only A0 is low
        Serial.println("14");
        down = 1;
      }
  if (down == 0) {
    Serial.println(0);  // 0 tells the host no button was down.
  }
}


