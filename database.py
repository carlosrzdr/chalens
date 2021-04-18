import sqlite3

class Database():

    def __init__(self, FILE = 'database.db', DEVICES_TABLE = 'devices', NETWORKS_TABLE = 'networks', KNOWN_TABLE = 'known'):
        self.FILE = FILE
        self.DEVICES_TABLE = DEVICES_TABLE
        self.KNOWN_TABLE = KNOWN_TABLE
        self.NETWORKS_TABLE = NETWORKS_TABLE
        self.connection = None

        try:
            self.connection = sqlite3.connect(FILE, check_same_thread=False)
        except Error as ex:
            print(ex)

        self.cursor = self.connection.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.DEVICES_TABLE}
                                (mac TEXT,
                                channel INTEGER,
                                signal INTEGER,
                                vendor TEXT,
                                bssid TEXT);
                                """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.NETWORKS_TABLE}
                                (bssid TEXT,
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

    def insertDevicesTable(self, mac, channel, signal, vendor, bssid):
        self.cursor.execute(f"""INSERT INTO {self.DEVICES_TABLE} (mac, channel, signal, vendor, bssid)
                                VALUES ('{mac}', {channel}, {signal}, '{vendor}', '{bssid}');
                                """)

        self.connection.commit()

    def insertNetworksTable(self, bssid, signal, vendor, ssid):
        self.cursor.execute(f"""INSERT INTO {self.NETWORKS_TABLE} (bssid, signal, vendor, ssid)
                                VALUES ('{bssid}', {signal}, '{vendor}', '{ssid}');
                                """)

        self.connection.commit()

    def getNetworksTable(self):
        self.cursor.execute(f"""SELECT *
                                FROM  {self.NETWORKS_TABLE}
                                """)

        results = self.cursor.fetchall()

        return results

    def getDevicesTable(self):
        self.cursor.execute(f"""SELECT *
                                FROM  {self.DEVICES_TABLE}
                                """)

        results = self.cursor.fetchall()

        return results