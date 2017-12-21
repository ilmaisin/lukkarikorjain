#!/home/protected/lukkari/bin/python

import cgi, cgitb, os
#cgitb.enable(display=0, logdir="/home/protected/lukkari_log")
cgitb.enable(format="plain")
form = cgi.FieldStorage()

os.write(1,b"Content-Type: text/plain\nCache-Control: max-age=21600\n\n") # CGI-otsakkeet

from icalendar import Calendar, Event
import urllib3, re, pytz
from datetime import datetime, timedelta
import urllib.parse as urlparse

def is_dst(querydate):
    return querydate.astimezone(pytz.timezone('Europe/Helsinki')).dst() != timedelta(0)

campus = form.getvalue("campus")
caldir = '/cal/' if campus in ['salo', 'ict'] else '/vcal/'

http = urllib3.PoolManager()
r = http.request('GET', 'http://lukkari.turkuamk.fi/' + campus + caldir + form.getvalue("group") + ".ics")
if r.status == 404:
    print('ERROR: Invalid campus or group')
    quit()

unicode_text = r.data.decode('latin1')
cal = Calendar.from_ical(unicode_text)

if form.getvalue("tidy") == "yes":
    cal.subcomponents[:] = [comp for comp in cal.subcomponents if comp['LOCATION'] != ""]

for e in cal.walk('vevent'):
    if is_dst(e['DTSTAMP'].dt) and not is_dst(e['DTSTART'].dt):
        e['DTSTART'].dt = e['DTSTART'].dt + timedelta(hours=1)
        e['DTEND'].dt = e['DTEND'].dt + timedelta(hours=1)
    elif not is_dst(e['DTSTAMP'].dt) and is_dst(e['DTSTART'].dt):
        e['DTSTART'].dt = e['DTSTART'].dt - timedelta(hours=1)
        e['DTEND'].dt = e['DTEND'].dt - timedelta(hours=1)

    e['SUMMARY'] = re.sub('^\[(.*?)\]\s', "", e['SUMMARY'])

if form.getvalue("insummary"):
    cal.subcomponents[:] = [comp for comp in cal.subcomponents if urlparse.unquote(form.getvalue("insummary")) in comp['SUMMARY']]

os.write(1,cal.to_ical())
