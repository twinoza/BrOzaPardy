""" This module is responsible for talking with Arduino board
"""

import serial
import time
import g

# Variable to define whether Arduino is being used or not
ARDUINO = True

if ARDUINO:
    usbport = '/dev/cu.usbmodem1421'
    ser = serial.Serial(usbport, 9600, timeout=0.1)

class arduinoTalker(object):
    """
    Class object for communication with Arudino device
    """
    def __init__(self):
        pass

    def checkup(self):
        if not ARDUINO:
            return
        #class method that waits until buttons are down to continue
        buttonsUp = False
        while not buttonsUp:
            out = self.contCheckForAnswer(0.5)
            if out=='0':
                buttonsUp = True
            else:
                print("-----\nButtons are down: {}"
                      "\n----\n".format( out))
                time.sleep(3)

        return

    def contCheckForAnswer(self, timeout1):
        #continuously check for answer until buzzer or timeout
        if not ARDUINO:
            time.sleep(3) #wait 3s (for dramatic testing)
            return '2' #dummy clicker
        startTime = time.time()
        msg = '0'
        while ((time.time() - startTime) < timeout1) and msg=='0':
            ser.write('S'.encode())
            tmpmsg = ser.readline()
            msg = str(tmpmsg[:-2]).split("'")[1] #hack for bytes/str split with python3
        return msg

    def checkDead(self):
        if not ARDUINO:
            return False
        ser.write('S')
        msg = ser.readline()
        if not msg:
            return True
        else:
            return False



