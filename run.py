""" This is single point and click approach for single questions
"""

from arduinoComm import arduinoTalker
import time
import g

team1 = 'Inglorious Thumbs'
team2 = 'Mango Lassi'
team3 = 'Golden State of Mind'
team4 = 'Dhangal'


clueShownTime = 15.
# clueAnsTime = 3.

teams = {team1:[2,3,4], team2:[5,6,7], team3:[8,9,10], team4:[11,12,14]}

def arduinoQuestionQueryThingFunction():
    at = arduinoTalker()
    print('Checking if buttons are up...')
    at.checkup() #wait until buttons are down to continue
    print('buttons are up!! Start clue in:')
    #NEAL: PRESENT THE CLUE HERE
    for i in range(3,0,-1):
        print(i)
        time.sleep(1)
    print('Go! (Timer for ',clueShownTime,' seconds started)')
    clueHappening = True
    while clueHappening:
        val = at.contCheckForAnswer(clueShownTime)
        if val=='0':
            print('Clue not answered in time. Moving on...')
            clueHappening=False
        else:
            #NEAL: REMOVE CLUE HERE
            for team, clickers in teams.items():
                if int(val) in clickers:
                    nowteam = team
            print('Buzzer ',val,' has been clicked! Team=',nowteam)
            clueHappening = False
    return


if __name__ == '__main__':
  arduinoQuestionQueryThingFunction()