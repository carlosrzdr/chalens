import subprocess
import redis

class Database():

    def __init__(self, interface='wlan1'):
        self.network_ssid = None
        self.interface = interface
 
        try:
            self.client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
            #self.client.flushdb()
        except Error as ex:
            print(ex)

        try:
            self.network_ssid = subprocess.Popen(f'sudo iwgetid {self.interface} --raw',
                                                    shell=True,
                                                    stdout=subprocess.PIPE,
                                                    universal_newlines=True).communicate()[0].strip()
            print(f"DB Log: Connected to {self.network_ssid}")
        except:
            print('DB Log: Not connected to any network!')

    def empty(self):
        self.client.flushdb()

    def getAPTable(self):
        keys = self.getAPTableKeys()
        values = []
        
        for key in keys:
            values.append(self.client.hgetall(key))

        # Ejemplo para excluir macs random
        # if self.client.hgetall(key)['mac'][1] not in ['2', '6', 'A', 'E']:
        #         values.append(self.client.hgetall(key))
        
        return values

    def getAPTableKeys(self):
        return self.client.keys("ap:*")

    def getDevicesInfo(self):
        keys = self.getDevicesTableKeys()
        values = []
        
        for key in keys:
            values.append(self.client.hgetall(key))
        
        return values

    def getDevicesChannels(self):
        keys = self.getDevicesTableKeys()
        values = [0]*14
        
        for key in keys:
            values[int(self.client.hgetall(key)['channel'])-1] += 1
        
        return values

    def getDevicesTableKeys(self):
        return self.client.keys("device:*")
