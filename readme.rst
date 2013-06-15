

====================================================
 Simple script to backup Fitbit data via Fitbit API
====================================================

Requirements
============

::

  -e git+https://github.com/orcasgit/python-fitbit.git#egg=python-fitbit


Setup
=====

1) get an API APP key on the Fitbit site: https://dev.fitbit.com/apps/new
2) authorize your app for your account: (see python-fitbit documentation: ``./fitbit/gather_keys_cli.py <con_key> <con_sec>`` )
3) write a credentials.py with the following content
::

  import datetime
  APP_KEY = ''
  APP_SECRET = ''
  USER_KEY = ''
  USER_SECRET = ''
  FILENAME = 'NAME.shelf'
  START_DATE = datetime.date(year=2013,month=6,day=1)

4) create directory "backup" for json-files


RUN
===

::

  python backup.py


FINAL WORDS
===========

There is lots of possibilities to improve this script and I am happy to merge pull requests.
For now this script backups my data and thats what I wanted.

