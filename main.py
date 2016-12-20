from flask import Flask, render_template
app = Flask(__name__)
temp = 10

@app.route('/')
def index():
    return render_template('index.html', timer = "0:15")

@app.route('/blank')
def blank(this):
	this.text = "that"
	return render_template('board.html')

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