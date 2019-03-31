import json
import os
import logging

class boardData:
	def __init__(self, val, ans, resp):
		self.val  = val
		self.ans  = ans
		self.resp = resp

	def append(cell):
		self[self.length] = cell

DB_FILENAME = 'testdb.json'
full_bd = []
curBd = []

if os.path.isfile(DB_FILENAME):
	full_bd = json.loads(open(DB_FILENAME).read())
	#print (full_bd)
else:
	print ("*****Oza utils.py: line 15 DB_FILENAME not found")
	#print (single)

	# iterate over 
	# for i in ["cat1","cat2","cat3","cat4","cat5","cat6"]:
	# 	pass #cell = single[0]
		#logging.info(cell)

def getBoard(rnd):
	for game in full_bd:
		
		print (game[0])
		gameType = game[0]["round"]
		print("gameType is :", gameType)
		
		
		if gameType == rnd:
			# need to save board to an instance of boardData
			curBd = game
			return game  # return the board if the gameType of this board matches variable rnd
	#logging.info(board)

	return []  # if no gameType match rnd, return blank []

def create_board(bdAns, bdClue):
	board = get_board()
	board.append(dict(ans=bdAns, clue=bdClue))

	open(DB_FILENAME, 'w+').write(json.dumps(board))

def get_ans():
	return "this is the answer"

def delete_note():
	pass