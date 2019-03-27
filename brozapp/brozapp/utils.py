import json
import os
import logging

class boardData:
	def __init__(self, val, ans, clue):
		self.val  = val
		self.ans  = ans
		self.clue = clue

DB_FILENAME = 'testdb.json'
full_bd = []
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

def get_board(rnd):
	for i in full_bd:
		#print (cellDict) #logging.info(cellDict)
		print (i[0])
		gameType = i[0]["round"]
		print("gameType is :%s", gameType)
		board = i
		#print (board)
		
		if gameType == rnd:
			return i
	#logging.info(board)

	return []  #json.loads(open(DB_FILENAME).read())

def create_board(bdAns, bdClue):
	board = get_board()
	board.append(dict(ans=bdAns, clue=bdClue))

	open(DB_FILENAME, 'w+').write(json.dumps(board))

def get_ans():
	return "this is the answer"

def delete_note():
	pass