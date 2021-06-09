import subprocess

class Selector():
    def __init__(self, interface='wlan0', unavailable_channels=1, max_channel=13):
        self.interface = interface
        self.current_channel = 0
        self.optimal_channel = None
        self.channelHopper = False
        self.unavailable_channels = unavailable_channels
        self.max_channel = max_channel

        self.checkChannel()
        

    def changeChannel(self, channel):
        subprocess.call('sudo iwconfig {} channel {}'.format(self.interface, channel), shell=True)
        self.current_channel = channel

    def checkChannel(self):
        try:
            channel_string = subprocess.check_output('sudo iwlist {} channel | grep Current'.format(self.interface), shell=True)
            channel = str(channel_string).split("(")[-1].replace("Channel ", "").replace(")\\n'", "")
            self.current_channel = int(channel)
        except:
            print("Not connected to any network!")

    def optimalChannel(self, devices_bytes, devices):
        score = [0]*self.max_channel

        if devices_bytes != score:
            for i in range(self.max_channel):
                score[i] = devices[i] + devices_bytes[i]/3000

            self.optimal_channel = score.index(min(score)) + 1

            if self.channelHopper:
                self.changeChannel(self.optimal_channel)
        else:
            self.optimal_channel = 'No data found!'

    def disableChannelHopper(self):
        self.channelHopper = False

    def enableChannelHopper(self):
        self.channelHopper = True