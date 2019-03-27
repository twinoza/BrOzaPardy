from flask import Blueprint, render_template, request, redirect
import glob
import logging
from brozapp.note_utils import get_board, create_board

bp = Blueprint(__name__, __name__, template_folder='templates')

# def fetch_notes():
# 	final_notes = []
# 	notes = glob.glob('noteapp/notes/*.note')

# 	for note in notes:
# 		with open(note) as _file:
# 			final_notes.append(_file.read())
# 		_file.close()
# 	return final_notes

@bp.route('/')
def list():
	return render_template('note_list.html', board=get_board())

@bp.route('/edit', methods=['POST', 'GET'])
def edit():
	if request.method == "POST":
		ans = request.form.get('note_title')
		clue = request.form.get('note_content')

		create_board(bdAns=ans, bdClue=clue)
		return redirect('/')

	return render_template('note_edit.html')

@bp.route('/valClicked', methods=['GET'])
def valClicked():
		return render_template('showAns.html') #, answer = get_ans() )

# @bp.route('/createnote', methods=['POST', 'GET'])
# def show():
# 	if request.method == 'POST':
# 		if request.form.get('createnote'):
# 			text = request.form.get('notetext')
			
# 			with open('noteapp/notes/{}.note'.format(random_string()), 'w+') as _file:
# 				_file.write(text)
# 			_file.close()

# 			return redirect('/')

# 	return render_template('note_edit.html')