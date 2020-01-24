from flask import render_template
from tracker_website import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html', title='Visualize', sidebar=['images', 'home', 'raw_data'])

@app.route('/raw_data')
def raw_data():
    return render_template('raw_data.html', title='Raw Data')

@app.route('/images')
def images():
    return render_template('images.html', title='Images')