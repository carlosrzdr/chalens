from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/network')
def network():
    return render_template('network.html')

@app.route('/area')
def area():
    return render_template('area.html')