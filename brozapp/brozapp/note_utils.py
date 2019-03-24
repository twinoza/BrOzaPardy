import json
import os

class board:
	def __init__(self, val, ans, clue):
		self.val  = val
		self.ans  = ans
		self.clue = clue

DB_FILENAME = 'testdb.json'

if os.path.isfile(DB_FILENAME):
	full_db = json.loads(open(DB_FILENAME).read())
	for i in ["cat1","cat2","cat3","cat4","cat5","cat6"]:
		


def get_board(type):
	if not os.path.isfile(DB_FILENAME):
		return []

	return json.loads(open(DB_FILENAME).read())

def create_board(bdAns, bdClue):
	board = get_board()
	board.append(dict(ans=bdAns, clue=bdClue))

	open(DB_FILENAME, 'w+').write(json.dumps(board))

def get_ans():
	return "this is the answer"

def delete_note():
	pass