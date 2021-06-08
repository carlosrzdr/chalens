import subprocess
import os
import signal

class Scan():
    def __init__(self, interface = 'wlan0'):
        self.proc = None
        self.running = False
        self.cmd = [f"trackerjacker -i {interface} --remove-unseen-devices --map"]

        subprocess.Popen(['pkill -f trackerjacker'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

    def enableScan(self):
        self.proc = subprocess.Popen(self.cmd, close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.running=True

    def disableScan(self):
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        subprocess.Popen(['pkill -f trackerjacker'], close_fds=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.running=False
