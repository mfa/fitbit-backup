import fitbit
import datetime
import shelve
import os
import json

# import credentials from extra file:
from credentials import (
    APP_KEY, APP_SECRET, USER_KEY, USER_SECRET, FILENAME,
    START_DATE
    )
# to get USER_KEY and USER_SECRET see
# http://python-fitbit.readthedocs.org/en/latest/

# START_DATE is a datetime.date-object


fb = fitbit.Fitbit(APP_KEY, APP_SECRET,
                   user_key=USER_KEY,
                   user_secret=USER_SECRET)

def get_shelf(filename=FILENAME):
    """ returns opened shelf
    """
    return shelve.open(filename)

def check(date, key):
    """ check if date and key are already in shelf
    """
    shelf = get_shelf()
    dt = date.strftime("%Y-%m-%d")
    skey = '%s-%s' % (dt, key)
    if skey in shelf.keys():
        print("Already downloaded: %s" % skey)
	return False
    return skey

def add_entry(skey, data):
    """ add entry to shelf and write a json-file each
    """
    shelf = get_shelf()
    print("Added: %s" % skey)
    shelf[skey] = data
    shelf.sync()
    with open(os.path.join("backup/", '%s.json' % skey), "w") as f:
        f.write(json.dumps(data))


def get_last_sync():
    """ return the time of last sync
    """
    d = fb.get_devices()
    if d:
        return datetime.datetime.strptime(d[0]['lastSyncTime'],
                                          '%Y-%m-%dT%H:%M:%S.%f')
    return None

def run():
    """ iterate over all days from start date till date of last sync
    """
    dtx = START_DATE
    # get time of last sync
    limit = get_last_sync()
    # download only until the day before the last sync
    while dtx < limit.date():
        # get sleep data
        skey = check(dtx, 'sleep')
        if skey:
            add_entry(skey, fb.sleep(dtx))
        # get activity data
        skey = check(dtx, 'activities')
        if skey:
            add_entry(skey, fb.activities(dtx))
        # add one day
        dtx += datetime.timedelta(days=1)

if __name__ == '__main__':
    run()
