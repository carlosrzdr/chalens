from flask import Flask, render_template
from database import Database
from scan import Scan

app = Flask(__name__)
db = Database()
sc = Scan(db)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/network')
def network():
    sc.read()
    regs = db.getDevicesTable()
    return render_template('network.html', **{"registry": regs})

@app.route('/area')
def area():
    return render_template('area.html')