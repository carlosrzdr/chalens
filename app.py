from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from scan import Scan
import os

app = Flask(__name__)
db = Database()
sc = Scan(db)

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
    db.empty()
    return redirect(url_for('index'))

@app.route('/network')
def network():
    regs = db.getDevicesTable()
    channels = db.getChannels()
    data=[]
    return render_template('network.html',  registry=regs,
                                            channels = channels,
                                            data=data,
                                            ncolor='rgba(50, 115, 220, 0.4)',
                                            gcolor='rgba(0, 205, 175, 0.4)',
                                            wcolor='rgba(255, 56, 96, 0.4)')

@app.route('/api/network')
def APInetwork():
    regs = db.getDevicesTable()
    return jsonify(regs)

@app.route('/refresh_area', methods=['POST'])
def refresh_area():
    return redirect(url_for('area'))

@app.route('/area')
def area():
    refresh_area()
    regs = db.getAPTable()
    return render_template('area.html', registry=regs)
