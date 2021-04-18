import sqlite3

class Database():

    def __init__(self, FILE = 'database.db', LAN_TABLE = 'lan', AREA_TABLE = 'area', KNOWN_TABLE = 'known'):
        self.FILE = FILE
        self.LAN_TABLE = LAN_TABLE
        self.KNOWN_TABLE = KNOWN_TABLE
        self.AREA_TABLE = AREA_TABLE
        self.connection = None

        try:
            self.connection = sqlite3.connect(FILE, check_same_thread=False)
        except Error as ex:
            print(ex)

        self.cursor = self.connection.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.LAN_TABLE}
                                (mac TEXT,
                                channel INTEGER,
                                signal INTEGER,
                                vendor TEXT,
                                bssid TEXT);
                                """)

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.AREA_TABLE}
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

    def insertLanTable(self, mac, channel, signal, vendor, bssid):
        self.cursor.execute(f"""INSERT INTO {self.LAN_TABLE} (mac, channel, signal, vendor, bssid)
                                VALUES ('{mac}', {channel}, {signal}, '{vendor}', '{bssid}');
                                """)

        self.connection.commit()

    def insertAreaTable(self, bssid, signal, vendor, ssid):
        self.cursor.execute(f"""INSERT INTO {self.AREA_TABLE} (bssid, signal, vendor, ssid)
                                VALUES ('{mac}', {signal}, '{vendor}', '{bssid}');
                                """)

        self.connection.commit()

    def getAreaTable(self):
        self.cursor.execute(f"""SELECT *
                                FROM  {self.AREA_TABLE}
                                """)

        results = self.cursor.fetchall()

        return results

    def getLanTable(self):
        self.cursor.execute(f"""SELECT *
                                FROM  {self.LAN_TABLE}
                                """)

        results = self.cursor.fetchall()

        return results