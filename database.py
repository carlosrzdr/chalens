import subprocess
import redis

class Database():

    def __init__(self, max_channel=13): 
        self.max_channel = max_channel
        try:
            self.client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
        except Error as ex:
            print(ex)

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
