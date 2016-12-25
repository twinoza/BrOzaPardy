from flask import Flask, request, render_template
import g, getOzaPardy as getOP
import opHelperFns as ophf
import logging

app = Flask(__name__)

# Initialize the values for boxes in OzaPardy
val = [ [i for i in range(100,600,100)],]*6

# Get the Jeopardy data from the TSV files
g.sBoard = getOP.getJeopardyData('Single', 'static/data/OzaPardy - Single.tsv')
g.dBoard = getOP.getJeopardyData('Double', 'static/data/OzaPardy - Double.tsv')
g.fBoard = getOP.getJeopardyData('Final', 'static/data/OzaPardy - Final.tsv')

# Teams are set up in g.py

@app.route('/', methods = ['POST', 'GET'])
def index():
    timer = "0:15"
    teams = g.Teams
    print("Hello from index in main.py")
    if request.method =='POST':
        btn = request.form
        currTeam = int(btn['hiddenTeamId'])
        teams[currTeam].name = btn['teamName']
        teams[currTeam].score = btn['teamScore']
    return render_template('index.html', **locals())

@app.route('/board/<sd>')   #  <sd> is single or double ozapardy
def drawBoard(sd):
  global val
  bdVal = val
  print(bdVal)
  teams = g.Teams
  cats = ["This & That", "That&This", "This", "That", "Everything", "Lots & Lots of Nothing Else & even more"]
  gmMulti = 1
  if sd == "d":
    gmMulti = 2
  return render_template( 'board.html', **locals() )

@app.route('/editTeam', methods=['POST'])
def editTeam():
  teams = g.Teams
  teamId = int(request.form['hiddenBtnId'])
  print("Team ID: ", teamId)
  return render_template('editTeam.html', **locals() )

@app.route('/clue/<cr>')   #  <RC> will be the clue number Row & Col 
def clue(cr):
  teams = g.Teams
  startTime = "5:00"

  if cr == "k":  # Time to display clock
    return render_template('klok.html', **locals() )

  col = int(int(cr)/10)
  row = int(int(cr)%10)
  
  clueText = g.boards[ophf.gmMode(g.gameMode)][ophf.boxId2boxNum(int(cr))].clue
  return render_template('clue.html', **locals() )

if __name__ == '__main__':
    app.run()
