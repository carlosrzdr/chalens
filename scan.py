import subprocess
import os
import signal
import yaml
from database import Database

class Scan():
    def __init__(self, interface = 'wlan0'):
        self.proc = None
        self.running = False
        self.network_ssid = None
        self.cmd = [f"trackerjacker -i {interface} --remove-unseen-devices --map"]

        subprocess.Popen(['pkill -f trackerjacker'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)


    def changeScan(self):
        if self.running:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            subprocess.Popen(['pkill -f trackerjacker'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
            self.running=False
        else:
            self.proc = subprocess.Popen(self.cmd, close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
            self.running=True
