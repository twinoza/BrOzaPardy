from flask import Flask, request, render_template
import logging
import ozaPardyClasses as opc
#import getOzaPardy

app = Flask(__name__)

val = [ [100]*6, [200]*6, [300]*6, [400]*6, [500]*6 ] # Initialize the boxes for OzaPardy

Team1 = opc.team(0, 'Team 1', 0000)
Team2 = opc.team(1, 'Team 2', 0000)
Team3 = opc.team(2, 'Team 3', 0000)
Team4 = opc.team(3, 'Team 4', 0000)
Teams = [Team1, Team2, Team3, Team4]

@app.route('/', methods = ['POST', 'GET'])
def index():
    timer = "0:15"
    teams = Teams
    print("Hello from index in main.py")
    if request.method =='POST':
        btn = request.form
        print(btn['teamName'], "POST MADE")
        currTeam = int(btn['hiddenTeamId'])  ### This line needs to be edited
        teams[currTeam].name = btn['teamName']
        teams[currTeam].score = btn['teamScore']

   	# teams[clickedTeam].name = request.form["#teamname"]
    return render_template('index.html', **locals())

@app.route('/board/<sd>')
def drawBoard(sd):
    global val
    bdVal = val
    teams = Teams
    cats = ["This & That", "That&This", "This", "That", "Everything", "Lots & Lots of Nothing Else & even more"]
    gmMulti = 1
    if sd == "d":
        gmMulti = 2
    return render_template( 'board.html', **locals() )

@app.route('/editTeam', methods =['POST'])
def editTeam():
	teams = Teams
	teamId = int(request.form['hiddenBtnId'])
	print("Team ID: ", teamId)
	return render_template('editTeam.html', **locals() )

@app.route('/updateTeamname')
def updateTeamname():
    return render_template('updateTeamname.html')

if __name__ == '__main__':
    app.run()
