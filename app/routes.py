from flask import current_app as app
from flask import jsonify
from .models import User

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Flask app!"})