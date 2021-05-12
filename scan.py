import subprocess
import os
import signal
import yaml
from database import Database

class Scan():
    def __init__(self, db, interface = 'wlan1'):
        self.proc = None
        self.running = False
        self.map_path='wifi_map.yaml'
        self.db = db
        self.cmd = [f"trackerjacker -i {interface} --map"]

        subprocess.Popen(['pkill -f trackerjacker'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

    def changeScan(self):
        if self.running:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            subprocess.Popen(['pkill -f trackerjacker'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
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

            if wifi_map:
                for ssid in wifi_map:
                    ssid_node = wifi_map[ssid]
                    bssid_node = list(ssid_node.keys())[0]
                    devices = ssid_node[bssid_node]['devices']
                    
                    for device in devices:
                        random_mac = True if device[1] in ['2','6','A','E'] else False
                        self.db.insertDevicesTable(device, devices[device]['channel'], devices[device]['signal'], devices[device]['vendor'], bssid_node, random_mac)

    def read_networks(self):
        if os.path.isfile(self.map_path):
            with open(self.map_path, 'r') as f:
                data = f.read()

            wifi_map = yaml.load(data, Loader=yaml.FullLoader)

            self.db.emptyTable(self.db.NETWORKS_TABLE)

            if wifi_map:
                for ssid in wifi_map:
                    ssid_node = wifi_map[ssid]
                    bssid_node = list(ssid_node.keys())[0]
                    
                    try:
                        channels = ssid_node[bssid_node]['channels']
                    except:
                        channels = []
                    
                    if bssid_node == '00:00:00:00:00:00':
                        self.db.insertNetworksTable(bssid_node, 'NULL', '', ssid, channels)
                    else:
                        self.db.insertNetworksTable(bssid_node, ssid_node[bssid_node]['signal'], ssid_node[bssid_node]['vendor'], ssid, channels)


