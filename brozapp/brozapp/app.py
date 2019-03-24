from flask import Flask
from brozapp.views.router import bp as router_bp
from brozapp.views.router import bp as valClicked_bp
# from brozapp.views.note_edit import bp as note_edit_bp

app = Flask(__name__)

# @app.route('/')
# def home():
# 	return "Hello There!!"

app.register_blueprint(router_bp)
app.register_blueprint(valClicked_bp)
# app.register_blueprint(note_edit_bp)