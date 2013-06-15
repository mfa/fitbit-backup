import fitbit
import datetime
import shelve
import os
import json

# import credentials from extra file:
from credentials import APP_KEY, APP_SECRET, USER_KEY, USER_SECRET
# to get USER_KEY and USER_SECRET see
# http://python-fitbit.readthedocs.org/en/latest/


fb = fitbit.Fitbit(APP_KEY, APP_SECRET,
                   user_key=USER_KEY,
                   user_secret=USER_SECRET)


def get_username():
    """ return the displayname of the user
    """
    d = fb.user_profile_get()
    if d:
        return d.get('user').get('displayName')
    return 'fallback'


def get_last_sync():
    """ return the time of last sync
    """
    d = fb.get_devices()
    if d:
        return datetime.datetime.strptime(d[0]['lastSyncTime'],
                                          '%Y-%m-%dT%H:%M:%S.%f')
    return None


def get_start_date():
    """ get date of user registration
    """
    d = fb.user_profile_get()
    if d:
        return datetime.datetime.strptime(d.get('user').get('memberSince'),
                                          '%Y-%m-%d').date()
    return datetime.date(year=2013, month=6, day=8)


def get_shelf():
    """ returns opened shelf
    """
    filename = "%s.shelf" % get_username()
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


def run():
    """ iterate over all days from start date till date of last sync
    """
    dtx = get_start_date()
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
