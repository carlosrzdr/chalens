import sqlite3
import subprocess

class Database():

    def __init__(self, FILE = 'database.db', NETWORKS_TABLE = 'networks', DEVICES_TABLE = 'devices', KNOWN_TABLE = 'known', interface='wlan0'):
        self.FILE = FILE
        self.KNOWN_TABLE = KNOWN_TABLE
        self.NETWORKS_TABLE = NETWORKS_TABLE
        self.DEVICES_TABLE = DEVICES_TABLE
        self.connection = None
        self.network_ssid = None
        self.interface = interface
        
        try:
            self.connection = sqlite3.connect(FILE, check_same_thread=False)
        except Error as ex:
            print(ex)

        try:
            self.network_ssid = subprocess.Popen(f'sudo iwgetid {self.interface} --raw',
                                                    shell=True,
                                                    stdout=subprocess.PIPE,
                                                    universal_newlines=True).communicate()[0].strip()
            print(f"Connected to {self.network_ssid}")
        except:
            print('Not connected to any network!')

        self.cursor = self.connection.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.DEVICES_TABLE}
                                (mac TEXT,
                                channel INTEGER,
                                signal INTEGER,
                                vendor TEXT,
                                bssid TEXT,
                                randomMac INTEGER);
                                """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.NETWORKS_TABLE}
                                (mac TEXT,
                                channels TEXT,
                                signal INTEGER,
                                vendor TEXT,
                                ssid TEXT);
                                """)
                            
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.KNOWN_TABLE}
                                (mac TEXT,
                                name TEXT);
                                """)

        self.connection.commit()

    def emptyTable(self, TABLE):
        self.cursor.execute(f"""DELETE FROM {TABLE};
                                """)

        self.connection.commit()

    def insertKnownTable(self, mac, name):
        self.cursor.execute(f"""INSERT INTO {self.KNOWN_TABLE} (mac, name)
                                VALUES ('{mac}', '{name}');
                                """)

        self.connection.commit()

    def insertDevicesTable(self, mac, channel, signal, vendor, bssid, random_mac):
        self.cursor.execute(f"""INSERT INTO {self.DEVICES_TABLE} (mac, channel, signal, vendor, bssid, randomMac)
                                VALUES ('{mac}', {channel}, {signal}, '{vendor}', '{bssid}', {random_mac});
                                """)

        self.connection.commit()

    def insertNetworksTable(self, bssid, signal, vendor, ssid, channels):
        self.cursor.execute(f"""INSERT INTO {self.NETWORKS_TABLE} (mac, signal, vendor, ssid, channels)
                                VALUES ('{bssid}', {signal}, '{vendor}', '{ssid}', '{channels}');
                                """)

        self.connection.commit()

    def getNetworksTable(self):
        self.cursor.execute(f"""SELECT mac, channels, signal, vendor, ssid
                                FROM  {self.NETWORKS_TABLE}
                                """)

        results = self.cursor.fetchall()

        return results

    def getDevicesOnNetworkTable(self):
        self.cursor.execute(f"""SELECT mac, channel, signal, vendor
                                FROM  {self.DEVICES_TABLE}
                                WHERE bssid IN (SELECT bssid
                                                FROM {self.NETWORKS_TABLE}
                                                WHERE ssid = '{self.network_ssid}')
                                    AND randomMac = 0
                                """)

        results = self.cursor.fetchall()

        return results

    def getChannels(self):
        self.cursor.execute(f"""SELECT channel, COUNT(channel)
                                FROM  {self.DEVICES_TABLE}
                                WHERE bssid IN (SELECT bssid
                                                FROM {self.NETWORKS_TABLE}
                                                WHERE ssid = '{self.network_ssid}')
                                GROUP BY channel
                                """)

        results = self.cursor.fetchall()

        channels = list(range(1, 15))
        channels_data = []

        for channel in channels:
            try:
                data = []
                chan = results[channel][0]
                for x in channels:
                    if x==chan:
                        data.append(results[channel][1])
                    else:
                        data.append(0)
            except:
                data=[0]*14
            
            channels_data.append(data)


        return channels, channels_data