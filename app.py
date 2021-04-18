from flask import Flask, render_template, request, jsonify
from database import Database
from scan import Scan

app = Flask(__name__)
db = Database()
sc = Scan(db)

@app.route('/')
@app.route('/home')
def index():
    if sc.running:
        return render_template('index.html', text='Up', type='success', btn='Apagar')
    else:
        return render_template('index.html', text='Down', type='danger', btn='Encender')

@app.route('/update_control', methods = ['POST'])
def update_control():
    if request.method == "POST":  # button selected
        btn = request.form["changeBtn"]
        return redirect(url_for("app.home"))

    return render_template('index.html', running_button=sc.running)

@app.route('/network')
def network():
    sc.read_devices()
    regs = db.getDevicesTable()
    return render_template('network.html', registry=regs)

@app.route('/area')
def area():
    sc.read_networks()
    regs = db.getNetworksTable()
    return render_template('area.html', registry=regs)