#!/env/bin/python
# encoding: utf-8

import sqlite3

def dict_factory(cursor, row):
    # by zhanglin encode to utf-8
    row = list(row)
    for i in range(len(row)):
        if type(row[i]) == type(u""):
            row[i] = row[i].encode("utf-8")
    row = tuple(row)

    d = {}

    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d

class CqwdtDBManager:
    """
    table station：
    Name            Declared    Type   Type    Size     Precision   Not Null    Not Null On Conflict    Default Value   Collate Position    Old Position
    city            CHAR        CHAR    0       0                   False                                                           0           0
    metro           CHAR        CHAR    0       0                   True                                                            1           1
    station_id      CHAR        CHAR    0       0                   True                                                            2           2
    station_name    CHAR        CHAR    0       0                   True                                                            3           3
    station_en      CHAR        CHAR    0       0                   False                                                           4           4
    transfer        CHAR        CHAR    0       0                   False                                                           5           5
    geo             CHAR        CHAR    0       0                   False                                                           6           6
    open_traffic    CHAR(1)     CHAR    1       0                   False                                                           7           7
    """
    def __init__(self, dbName):
        self.db = sqlite3.connect("./DBDATA/cqwdt.db")
        self.db.row_factory = dict_factory
        self.c = self.db.cursor()

    # 根据车站编号进行查询
    # def select_station_by_station_id(self, station_id):
    #     return self.c.execute("SELECT * FROM station st WHERE st.station_id = {0}".format(station_id)).fetchall()

    # 根据车站名称进行查询
    def select_station_by_station_name(self, station_name):
        return self.c.execute("SELECT * FROM station st LEFT JOIN schedule sc ON st.station_id = sc.station_id WHERE st.station_name = '{0}' ORDER BY station_id".format(station_name)).fetchall()

    # 根据车站名称进行模糊查询
    def select_station_like_station_name(self, station_name):
        return self.c.execute("SELECT * FROM station st WHERE st.station_name LIKE '%{0}%'".format(station_name)).fetchall()
 
    def closeDB(self):
        self.db.commit()
        self.db.close()

