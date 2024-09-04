import sqlite3
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar, json
from random import randint

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_conection(data='database/motif_traf.db'):
    conn = sqlite3.connect(data)
    conn.row_factory = dict_factory
    return conn
