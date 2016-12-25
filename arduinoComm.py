""" This module is responsible for talking with Arduino board
"""

import serial
import time
import g

# Variable to define whether Arduino is being used or not
ARDUINO = True

if ARDUINO:
    usbport = '/dev/cu.usbmodem1411'
    ser = serial.Serial(usbport, 9600, timeout=0.1)

clueTime = 15.
clueAnsTime = 15.

class arduinoTalker(object):
    """
    Class object for communication with Arudino device
    """
    def __init__(self):
        pass

    def checkup(self):
        #class method that waits until buttons are down to continue
        buttonsUp = False
        while not buttonsUp:
            out = self.contcheckforanswer(0.5)
            if out=='0':
                buttonsUp = True
        return

    def contcheckforanswer(self, timeout1):
        #continuously check for answer until buzzer or timeout
        startTime = time.time()
        msg = '0'
        while ((time.time() - startTime) < timeout1) and msg=='0':
            ser.write('S')
            msg = ser.read()
        return msg



