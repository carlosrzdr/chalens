from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from scan import Scan
import os

app = Flask(__name__)
db = Database()
sc = Scan()

@app.route('/')
@app.route('/home')
def index():
    else:
        return render_template('index.html')

@app.route('/erase_data', methods=['POST'])
def erase_data():
    db.empty()
    return redirect(url_for('index'))

@app.route('/devices')
def devices():
    return render_template('devices.html')

@app.route('/area')
def area():
    refresh_area()
    regs = db.getAPTable()
    return render_template('area.html', registry=regs)

@app.route('/api/devices_info')
def API_DevicesInfo():
    regs = db.getDevicesInfo()
    return jsonify(regs)

@app.route('/api/devices_channels')
def API_DevicesChannels():
    regs = db.getDevicesChannels()
    return jsonify(regs)

@app.route('/api/scan')
def API_Scan():
    regs = {'running': sc.running}
    return jsonify(regs)

@app.route('/api/enable_scan', methods=['POST'])
def API_EnableScan():
    sc.enableScan()
    print('Sniffing started!')
    return redirect(url_for('index'))

@app.route('/api/disable_scan', methods=['POST'])
def API_DisableScan():
    sc.disableScan()
    print('Sniffing stopped!')
    return redirect(url_for('index'))
