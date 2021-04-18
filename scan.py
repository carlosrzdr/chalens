import subprocess
import os
import signal
import yaml
from database import Database

class Scan():
    def __init__(self, db, interface = 'wlan0'):
        self.proc = None
        self.map_path='wifi_map.yaml'
        self.db = Database()
        self.cmd = [f"trackerjacker -i {interface} --map"]

    def startScan(self):
        self.proc = subprocess.Popen(self.cmd, close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

    def stopScan(self):
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)

    def read_lan(self):
        with open(self.map_path, 'r') as f:
            data = f.read()

        wifi_map = yaml.load(data, Loader=yaml.FullLoader)

        for ssid in wifi_map:
            ssid_node = wifi_map[ssid]
            bssid_node = list(ssid_node.keys())[0]
            devices = ssid_node[bssid_node]['devices']
            
            for device in devices:
                self.db.insertLanTable(device, devices[device]['channel'], devices[device]['signal'], devices[device]['vendor'], bssid_node)

    def read_area(self):
        with open(self.map_path, 'r') as f:
            data = f.read()

        wifi_map = yaml.load(data, Loader=yaml.FullLoader)

        for ssid in wifi_map:
            ssid_node = wifi_map[ssid]
            bssid_node = list(ssid_node.keys())[0]
            devices = ssid_node[bssid_node]['devices']

            self.db.insertAreaTable(bssid_node, ssid_node[bssid_node]['signal'], ssid_node[bssid_node]['vendor'], ssid_node)


