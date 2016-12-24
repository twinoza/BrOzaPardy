from flask import Flask, request, render_template
import g, getOzaPardy as getOP
import logging

app = Flask(__name__)

val = [ [100]*6, [200]*6, [300]*6, [400]*6, [500]*6 ] # Initialize the boxes for OzaPardy

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

@app.route('/board/<sd>')
def drawBoard(sd):
    global val
    bdVal = val
    teams = g.Teams
    cats = ["This & That", "That&This", "This", "That", "Everything", "Lots & Lots of Nothing Else & even more"]
    gmMulti = 1
    if sd == "d":
        gmMulti = 2
    return render_template( 'board.html', **locals() )

@app.route('/editTeam', methods =['POST'])
def editTeam():
	teams = g.Teams
	teamId = int(request.form['hiddenBtnId'])
	print("Team ID: ", teamId)
	return render_template('editTeam.html', **locals() )

@app.route('/updateTeamname')
def updateTeamname():
    return render_template('updateTeamname.html')

if __name__ == '__main__':
    app.run()
