import requests
import sys
import sqlite3
import pandas as pd
import time
import datetime
import json
import logging

excel = sys.argv[1]

df = pd.read_excel(excel)
data_fetch = df[df.fetch == 1]

f = open('settings.txt', 'r')
splitted = f.read().splitlines()
f.close()
to = int(splitted[0].split('-')[1])
path_err = splitted[1].split('-')[1].replace(' ', '')
path_log = splitted[2].split('-')[1].replace(' ', '')
path_sql = splitted[3].split('-')[1].replace(' ', '')

logging.basicConfig(filename=path_log, level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logging.info('Start of the script')

error = []
conn = sqlite3.connect(path_sql)
cursor = conn.cursor()

for i in range(len(data_fetch)):
    try:
        url = data_fetch.iloc[i]['url']
        logging.debug('Sending request to %s' % url)
        t1 = time.time()
        ts = datetime.datetime.now()
        label = data_fetch.iloc[i]['label']
        r = requests.get(url, timeout=to)
        resp_time = time.time() - t1
        status = r.status_code
        if status == 200:
            insert = """INSERT INTO MONITORING
                        (TS, URL, LABEL, RESPONSE_TIME,
                        STATUS_CODE, CONTENT_LENGTH)
                        VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (ts, url, label, resp_time, status, len(r.text))
            cursor.execute(insert, data_tuple)
            conn.commit()
        else:
            insert = """INSERT INTO MONITORING
                        (TS, URL, LABEL, RESPONSE_TIME,
                        STATUS_CODE, CONTENT_LENGTH)
                        VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (ts, url, label, resp_time, status, None)
            cursor.execute(insert, data_tuple)
            conn.commit()
        logging.debug("Request completed with code %i" % status)
    except Exception:
        logging.debug("")
        exc_tuple = sys.exc_info()
        err = dict()
        err['timestamp'] = ts
        err['url'] = url
        err['error'] = {"exception_type": exc_tuple[0],
                        "exception_value": exc_tuple[1],
                        "stack_info": exc_tuple[2]}
        error.append(err)
        logging.debug("Request failed")
file_object = open(path_err, 'w')
json.dump(error, file_object, indent=4, sort_keys=True, default=str)
file_object.close()

logging.info('End of the script')
conn.close()
