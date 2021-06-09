from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from scan import Scan
from selector import Selector
import os

app = Flask(__name__)
db = Database()
sc = Scan()
selector = Selector()
db.empty()

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/erase_data', methods=['POST'])
def erase_data():
    db.empty()
    selector.optimal_channel = None
    return redirect(url_for('index'))

@app.route('/devices')
def devices():
    return render_template('devices.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/api/devices_info')
def API_DevicesInfo():
    regs = db.getDevicesInfo()
    return jsonify(regs)

@app.route('/api/devices_channels')
def API_DevicesChannels():
    regs = db.getDevicesChannels()
    return jsonify(regs)

@app.route('/api/devices_bytes')
def API_DevicesBytes():
    regs = db.getDevicesBytes()
    return jsonify(regs)

@app.route('/api/scan')
def API_Scan():
    regs = {'running': sc.running}
    return jsonify(regs)

@app.route('/api/enable_scan', methods=['POST'])
def API_EnableScan():
    sc.enableScan()
    print('Sniffing started!')
    return jsonify({'status': 'ok'})

@app.route('/api/disable_scan', methods=['POST'])
def API_DisableScan():
    sc.disableScan()
    print('Sniffing stopped!')
    return jsonify({'status': 'ok'})

@app.route('/api/channel')
def API_Channel():
    selector.checkChannel()
    regs = {'channel': selector.current_channel}
    return jsonify(regs)

@app.route('/api/optimal_channel')
def API_GetOptimalChannel():
    selector.optimalChannel(db.getDevicesBytes(), db.getDevicesChannels())
    regs = {'channel': selector.optimal_channel}
    return jsonify(regs)

@app.route('/api/change_channel', methods=['POST'])
def API_ChangeChannel():
    channel = request.form['channel']
    try:
        channel = int(channel)
    except:
        return jsonify({'status': 'ko'})

    selector.changeChannel(channel)
    return jsonify({'status': 'ok'})

@app.route('/api/hop')
def API_Hop():
    regs = {'hop': selector.channelHopper}
    return jsonify(regs)

@app.route('/api/enable_channel_hopper', methods=['POST'])
def API_EnableChannelHopper():
    selector.enableChannelHopper()
    print('Enable channel hopping!')
    return jsonify({'status': 'ok'})

@app.route('/api/disable_channel_hopper', methods=['POST'])
def API_DisableChannelHopper():
    selector.disableChannelHopper()
    print('Disable channel hopping!')
    return jsonify({'status': 'ok'})
