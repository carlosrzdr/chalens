from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from scan import Scan
import os
import numpy as np

app = Flask(__name__)
db = Database()
sc = Scan(db)

n, bins = 10000, 20
normal = np.random.normal(0, 1, n)
gumbel = np.random.gumbel(0, 1, n)
weibull = np.random.weibull(5, n)
nhistogram = np.histogram(normal, bins=bins)
ghistogram = np.histogram(gumbel, bins=bins)
whistogram = np.histogram(weibull, bins=bins)

@app.route('/')
@app.route('/home')
def index():
    if sc.running:
        return render_template('index.html', text='Escaneando', textType='success', btnType='danger', btn='Apagar')
    else:
        return render_template('index.html', text='Apagado', textType='danger', btnType='success', btn='Encender')

@app.route('/update_control', methods=['POST'])
def update_control():
    sc.changeScan()
    print('Sniffing started!') if sc.running else print('Sniffing stopped!')
    return redirect(url_for('index'))

@app.route('/erase_data', methods=['POST'])
def erase_data():
    if os.path.exists("wifi_map.yaml"):
        os.remove("wifi_map.yaml")
    db.emptyTable(db.DEVICES_TABLE)
    db.emptyTable(db.NETWORKS_TABLE)
    return redirect(url_for('index'))

@app.route('/refresh_network', methods=['POST'])
def refresh_network():
    sc.read_devices()
    return redirect(url_for('network'))

@app.route('/refresh_area', methods=['POST'])
def refresh_area():
    sc.read_networks()
    return redirect(url_for('area'))

@app.route('/network')
def network():
    refresh_network()
    regs = db.getDevicesOnNetworkTable()
    chan = db.getChannels()
    return render_template('network.html',  registry=regs,
                                            channels = chan,
                                            nvalues=nhistogram[0].tolist(),
                                            nlabels=nhistogram[1].tolist(),
                                            ncolor='rgba(50, 115, 220, 0.4)',
                                            gvalues=ghistogram[0].tolist(),
                                            glabels=ghistogram[1].tolist(),
                                            gcolor='rgba(0, 205, 175, 0.4)',
                                            wvalues=whistogram[0].tolist(),
                                            wlabels=whistogram[1].tolist(),
                                            wcolor='rgba(255, 56, 96, 0.4)')

@app.route('/area')
def area():
    refresh_area()
    regs = db.getNetworksTable()
    return render_template('area.html', registry=regs)

@app.route('/select_device')
def select_device(methods=['GET']):
    print('Dispositivo escogido: ', request.args.getlist('device'))
    return redirect(url_for('network'))
