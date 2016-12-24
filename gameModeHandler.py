""" This module controls the gameMode logic and functionality.
    It also ???
"""

import serial
import time
import g

# Variable to define whether Arduino is being used or not
ARDUINO = False

if ARDUINO:
    usbport = '/dev/cu.usbmodem1411'
    ser = serial.Serial(usbport, 9600, timeout=0.1)

clueTime = 15.
clueAnsTime = 15.

def arduinoQuestionQueryThingFunction():
    # Wait for buttons to be up
    buttonsUp = False
    while not buttonsUp:
        out = keepCheckingForAnswer(1.)
        if out=='0':
            buttonsUp = True
        print("Check the buttons, dumbo!")
    clueIsShown = True
    while clueIsShown:
        #NEAL: present the clue on the button here

        #now counting down and check for button press in clueTime
        out = keepCheckingForAnswer(clueTime)
        if out!='0':
            #NEAL: take the clue off the button here!

            #now the user has clueAnsTime to answer
            startAnsTime = time.time()
            answered = False
            while ((time.time()-startAnsTime) < clueAnsTime) and not answered:
                #NEAL: when clue is answered set answered to True
                #NEAL:if answered correctly:
                #NEAL:   score positive points for that team
                #NEAL:   set clueIsShown = False
                #NEAL:elif answered incorrectly:
                #NEAL:   deduct points from the team
                print('hey')
        else:
            clueIsShown = False #kill the clue because no one answered
    return


def keepCheckingForAnswer(timeout1):
    startTime = time.time()
    msg = '0'
    while ((time.time() - startTime) < timeout1) and msg=='0':
        ser.write('S')
        # time.sleep(0.050) #50 ms of sleep to allow time to read
        # time.sleep(5)
        msg = ser.read()
    return msg

