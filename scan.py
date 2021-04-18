import subprocess
import os
import signal
import yaml
from database import Database

class Scan():
    def __init__(self, db, interface = 'wlan0'):
        self.proc = None
        self.running = False
        self.map_path='wifi_map.yaml'
        self.db = db
        self.cmd = [f"trackerjacker -i {interface} --map"]

    def changeScan(self):
        if self.running:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            self.running=False
        else:
            self.proc = subprocess.Popen(self.cmd, close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
            self.running=True

    def read_devices(self):
        if os.path.isfile(self.map_path):
            with open(self.map_path, 'r') as f:
                data = f.read()

            wifi_map = yaml.load(data, Loader=yaml.FullLoader)

            self.db.emptyTable(self.db.DEVICES_TABLE)

            for ssid in wifi_map:
                ssid_node = wifi_map[ssid]
                bssid_node = list(ssid_node.keys())[0]
                devices = ssid_node[bssid_node]['devices']
                
                for device in devices:
                    self.db.insertDevicesTable(device, devices[device]['channel'], devices[device]['signal'], devices[device]['vendor'], bssid_node)

    def read_networks(self):
        if os.path.isfile(self.map_path):
            with open(self.map_path, 'r') as f:
                data = f.read()

            wifi_map = yaml.load(data, Loader=yaml.FullLoader)

            self.db.emptyTable(self.db.NETWORKS_TABLE)

            for ssid in wifi_map:
                ssid_node = wifi_map[ssid]
                bssid_node = list(ssid_node.keys())[0]
                if bssid_node == '00:00:00:00:00:00':
                    self.db.insertNetworksTable(bssid_node, 'NULL', '', ssid)
                else:
                    self.db.insertNetworksTable(bssid_node, ssid_node[bssid_node]['signal'], ssid_node[bssid_node]['vendor'], ssid)


