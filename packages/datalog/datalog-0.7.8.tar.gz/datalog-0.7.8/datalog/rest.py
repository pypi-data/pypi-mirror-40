import time
import logging
from bottle import route, run, get, abort
import json

import datalog

# datastore object used for REST requests
datastore = None

# maximum requested readings
MAX_AMOUNT = 1000

start_time = None

def run_server(ds):
    global datastore, start_time

    # save datastore
    datastore = ds

    # start it
    logging.getLogger("rest-server").info("Starting web server")

    # set start time
    start_time = int(round(time.time() * 1000))

    # create server
    run(host='localhost', port=8080)

    logging.getLogger("rest-server").info("Web server stopped")

@get
def latest(fmt="json", amount=1000):
    return handle_fixed_list(fmt=fmt, amount=amount, desc=True)

@get
def earliest(fmt="json", amount=1000):
    return handle_fixed_list(fmt=fmt, amount=amount, desc=False)

def handle_fixed_list(fmt, amount, desc):
    global datastore, MAX_AMOUNT

    fmt = str(fmt)
    amount = int(amount)

    if amount > MAX_AMOUNT:
        amount = MAX_AMOUNT

    if fmt == "json":
        return datastore.json_repr(amount=amount, desc=desc)
    elif fmt == "csv":
        return datastore.csv_repr(amount=amount, desc=desc)
    else:
        abort(400, "Invalid format")

@get
def info(fmt="json"):
    global start_time

    # uptime
    up_time = int(round(time.time() * 1000)) - start_time

    data = {
        'server_version': datalog.__version__,
        'start_time': start_time,
        'up_time': up_time
    }

    if fmt == "json":
        return json.dumps(data)
    elif fmt == "csv":
        return "\n".join(["\"{}\",\"{}\"".format(key, val) for key, val in data.items()])
    else:
        abort(400, "Invalid format")
