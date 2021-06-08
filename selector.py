import subprocess

class Selector():
    def __init__(self, interface='wlan0'):
        self.interface = interface
        self.current_channel = 0
        self.optimal_channel = None
        self.channelHopper = False

        try:
            self.current_channel = 2
        except:
            print("Not connected to any network!")

    def changeChannel(self, channel):
        subprocess.call('iw dev {} set channel {}'.format(self.interface, channel), shell=True)
        self.current_channel = channel

    def optimalChannel(self, devices_bytes, devices):
        score = [0]*14

        if devices_bytes != score:
            for i in range(len(devices_bytes)):
                score[i] = devices[i] + devices_bytes[i]/1000

            self.optimal_channel = score.index(min(score)) + 1

            if self.channelHopper:
                changeChannel(self.optimal_channel)
        else:
            self.optimal_channel = 'No data found!'

    def disableChannelHopper(self):
        self.channelHopper = False

    def enableChannelHopper(self):
        self.channelHopper = True