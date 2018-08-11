Lukkarikorjain
==============

Notice: This repository is now considered obsolete as TUAS has discontinued the use of Mimosa scheduling software. It is kept available as an archive for possible use at other institutions still using Mimosa. 

This is a really simple Python CGI script that does some things to fix the iCalendar output of the Mimosa scheduling software. This is configured for use in Turku University of Applied Sciences where I am studying, but probably can be adapted to be used elsewhere.

Modifications that are done to the output
-----------------------------------------

- Fixes the daylight saving problem. Due to a bug in the software, when the schedule is generated before daylight saving starts, the lessons after the beginning of DST are marked one hour too late and vice versa.

- Translates the character set to UTF-8 which is the preferred encoding in iCalendar.

- Removes the calendar title that is repeated in square bracket on every event's summary. That is probably redundant as most calendaring software can mark different calendars anyway for example by color-coding.

Hosted version
--------------
The script is (not anymore) hosted at http://lukkari.iirolaiho.net/. You need to pass your campus and personnel/group identifier in the query string. For example, if you want the schedule of NPROMS14yt, you should enter `http://lukkari.iirolaiho.net/lukkari.py?campus=lemminkaisenkatu&group=nproms14yt` to your calendaring software's URL field.
