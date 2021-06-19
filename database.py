import subprocess
import redis
from datetime import datetime
import subprocess
import os
class Database():

    def __init__(self, max_channel=13): 
        self.max_channel = max_channel
        try:
            self.client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
        except Error as ex:
            print(ex)

    def empty(self):
        self.client.flushdb()

    def save(self):
        dirName = os.getcwd() + '/../data'
        if not os.path.exists(dirName):
            os.makedirs(dirName)
            subprocess.Popen(["chmod 777 {}".format(dirName)], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print("Directory", dirName, "created ")
        else:    
            print("Directory", dirName, "already exists")
        filepath = dirName + "/devices_info_{}.csv".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        data = self.getDevicesInfo()

        with open(filepath, 'w') as f:
            f.writelines('mac;vendor;signal;last_seen;channel;time;bssid;bytes')
            for entry in data:
                f.writelines("{};{};{};{};{};{};{};{}\n".format(entry['mac'], entry['vendor'], entry['signal'], entry['last_seen'], entry['channel'], entry['time'], entry['bssid'], entry['bytes']))

        subprocess.Popen(["chmod 777 {}".format(filepath)], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def getAPTable(self):
        keys = self.getAPTableKeys()
        values = []
        
        for key in keys:
            values.append(self.client.hgetall(key))
        
        return values

    def getAPTableKeys(self):
        return self.client.keys("ap:*")

    def getDevicesInfo(self):
        keys = self.getDevicesTableKeys()
        values = []
        
        for key in keys:
            info = self.client.hgetall(key)
            if info['mac'][1] in ['2', '6', 'A', 'E']:
                info['vendor'] = 'Random MAC'
            values.append(info)
        
        return values

    def getDevicesChannels(self):
        keys = self.getDevicesTableKeys()
        values = [0]*self.max_channel
        
        for key in keys:
            values[int(self.client.hgetall(key)['channel'])-1] += 1
        
        return values

    def getDevicesBytes(self):
        keys = self.getDevicesTableKeys()
        values = [0]*self.max_channel
        
        for key in keys:
            device = self.client.hgetall(key)
            values[int(device['channel'])-1] += int(device['bytes'])
        
        return values

    def getDevicesTableKeys(self):
        return self.client.keys("device:*")
