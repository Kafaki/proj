from flask import Blueprint

app_route = Blueprint('route', __name__)

@app_route.route('/')
def index():
	return 'Hello world!'

@app_route.route('/new')
def new():
	return 'Hello/ new!'