import sys
import sqlite3
import requests
from datetime import date, timedelta

def get_data_for_date(db, d):

    conn = sqlite3.connect(db)
    c = conn.cursor()
    delta = timedelta(days=1)
    dt = date.today() - delta * d
    c.execute('select count(*) from quotes where dt = ?', (dt.isoformat(),))

    if c.fetchone()[0] > 0:
        conn.close()
        return

    url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities.json?date='
    start = 0

    while True:
        r = requests.get(url + dt.isoformat() + '&start=' + str(start))
        data = r.json()['history']['data']
        page = r.json()['history.cursor']['data'][0]
        arr = []

        for d in data:
            arr.append((d[1], d[2], d[3], d[6], d[7], d[8], d[11], d[12]))

        c.executemany('''
        INSERT INTO quotes (dt, name, ticker, open, low, high, close, vol) 
        VALUES (?,?,?,?,?,?,?,?)
        ''', arr)
        start += 100

        if start > page[1]:
            break

    conn.commit()
    conn.close()

if __name__ == '__main__':
    start = 0
    end = 1

    try:
        if len(sys.argv) == 2:
            end = int(sys.argv[1])
        if len(sys.argv) == 3:
            start = int(sys.argv[1])
            end = int(sys.argv[2])
    except:
        print('Incorrect values for days count!')

    for i in range(start, end):
        get_data_for_date('trade.db', i)

