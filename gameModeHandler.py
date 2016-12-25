""" This module controls the gameMode logic and functionality.
"""

from arduinoComm import arduinoTalker
import time
import g


def arduinoQuestionQueryThingFunction():
    at = arduinoTalker()
    at.checkup() #wait until buttons are down to continue
    #NEAL: PRESENT THE CLUE HERE

    questionHappening = True
    while questionHappening:
        val = at.contcheckforanswer()
        if val=='0':
            print('Clue not answered in time. Moving on...')
            questionHappening=False
        else:
            #NEAL: REMOVE CLUE HERE

            print('Buzzer ',val,' has been clicked!')
            startAnsTime = time.time()
            answered = False
            while ((time.time()-startAnsTime) < clueAnsTime) and not answered:
                #NEAL: when clue is answered set answered to True
                #NEAL:if answered correctly:
                #NEAL:   score positive points for that team
                #NEAL:   set clueIsShown = False
                #NEAL:elif answered incorrectly:
                #NEAL:   deduct points from the team, added clue back to screen 
                print('hey')

    return


