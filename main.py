from flask import Flask, render_template
import logging
import ozaPardyClasses as opc

app = Flask(__name__)
temp = 0
# Initialize the boxes for OzaPardy

Team1 = opc.team('Mice', 2500)
Team2 = opc.team('Men', 2200)
Teams = [Team1, Team2]

@app.route('/')
def index():
    global Teams
    timer = "0:15"
    Teams[1].score += 100
    return render_template('index.html', **locals())

@app.route('/board/<sd>')
def drawBoard(sd):
    cats = ["This & That", "That&This", "This", "That", "Everything", "Lots & Lots of Nothing Else"]
    gmMulti = 1
    if sd == "d":
        gmMulti = 2
    return render_template( 'board.html', **locals() )

@app.route('/home')
def drawHome():
    global temp
    temp = temp + 1
    return render_template('home.html', number = temp)

if __name__ == '__main__':
    app.run()
