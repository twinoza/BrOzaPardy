from flask import Flask, render_template
import logging
import ozaPardyClasses as opc
import getOzaPardy

app = Flask(__name__)

val = [ [100]*6, [200]*6, [300]*6, [400]*6, [500]*6 ] # Initialize the boxes for OzaPardy

Team1 = opc.team('Mice', 2500)
Team2 = opc.team('Men', 2200)
Team3 = opc.team('None', 0000)
Team4 = opc.team('None', 0000)
Teams = [Team1, Team2, Team3, Team4]

@app.route('/')
def index():
    global Teams
    timer = "0:15"
    teams = Teams
    return render_template('index.html', **locals())

@app.route('/board/<sd>')
def drawBoard(sd):
    global val
    bdVal = val
    teams = Teams
    cats = ["This & That", "That&This", "This", "That", "Everything", "Lots & Lots of Nothing Else"]
    gmMulti = 1
    if sd == "d":
        gmMulti = 2
    return render_template( 'board.html', **locals() )

@app.route('/getTeamname')
def getTeamname():
	teams = Teams
	return render_template('getTeamname.html' **locals() )

@app.route('/updateTeamname')
def updateTeamname():
    return render_template('updateTeamname.html')

if __name__ == '__main__':
    app.run()
