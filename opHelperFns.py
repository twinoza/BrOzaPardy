import textwrap

def myWrap(inStr):
    ''' Wraps text
        inStr: input string that needs to be wrapped
        tmp: temporary string that has the output
    '''
    tmp = textwrap.wrap(inStr, 30)
    tmp = '\n'.join(tmp) 
    return tmp

"""
Sorry Neal, we are putting the query function here...
"""

import serial
import time

usbport = '/dev/cu.usbmodem1411'

question_time = 30.
question_ans_time = 20.

def ArduinoQuestionQueryThingFunction():
    #wait for buttons to be up
    buttonsup = False
    while not buttonsup:
        out = keep_checking_for_answer(1.)
        if out=='0':
            buttonsup = True
        print("Check the buttons, dumbo!")
    question_is_happening = True
    while question_is_happening:
        #NEAL: present the question on the button here

        #now counting down and check for button press in question_time
        out = keep_checking_for_answer(question_time)
        if out!='0':
            #NEAL: take the question off the button here!

            #now the user has question_ans_time to answer the question
            start_ans_time = time.time()
            answered = False
            while ((time.time()-start_ans_time) < question_ans_time) and not answered:
                #NEAL: when question is answered set answered to True
                #NEAL:if answered correctly:
                #NEAL:   score positive points for that team
                #NEAL:   set question_is_happening = False
                #NEAL:elif answered incorrectly:
                #NEAL:   deduct points from the team
                print 'hey'
        else:
            question_is_happening = False #kill the question because no one answered
    return

def keep_checking_for_answer(timeout1):
    ser = serial.Serial(usbport, 9600, timeout=0.1)
    start_time = time.time()
    msg = '0'
    while ((time.time() - start_time) < timeout1) and msg=='0':
        ser.write('S')
        msg = ser.read()
    return msg


