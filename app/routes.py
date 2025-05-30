from flask import current_app as app
from flask import render_template
from .add_base_data import add_base_data
from .models import user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_base_data')
def add_base_data_route():
    """
    Route to add base data to the database.
    """
    add_base_data()
    return render_template('index.html')