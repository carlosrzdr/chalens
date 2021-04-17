import subprocess
import os
import yaml
from database import Database

class Scan():
    def __init__(self, db):
        self.proc = subprocess.Popen(['trackerjacker -i wlan0 --map'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        self.map_path='wifi_map.yaml'
        self.db = db

    def read(self):
        with open(self.map_path, 'r') as f:
            data = f.read()

        wifi_map = yaml.load(data, Loader=yaml.FullLoader)

        for ssid in wifi_map:
            ssid_node = wifi_map[ssid]
            bssid_node = list(ssid_node.keys())[0]
            devices = ssid_node[bssid_node]['devices']
            
            for device in devices:
                self.db.insertDevicesTable(device, devices[device]['channel'], devices[device]['signal'], devices[device]['vendor'], bssid_node)

            break


