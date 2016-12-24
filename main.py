from flask import Flask, request, render_template
import g, getOzaPardy as getOP
import logging

app = Flask(__name__)

val = [ [i for i in range(100,600,100)],]*6 # Initialize the boxes for OzaPardy

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
  col = int(int(cr)/10)
  row = int(int(cr)%10)
  cv = "He was the President of USA for last 8 years and these were the last 8 Presidents of USA and Prime Ministers of India"
  return render_template('clue.html', **locals() )

if __name__ == '__main__':
    app.run()
