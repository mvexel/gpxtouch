gpxtouch.py

Takes one or more GPX XML files as argument and sets the modification
and access times to the timestamp of the most recent trackpoint of 
each GPX file.

Sample usages:

* gpxtouch.py long_walk_long_ago.gpx
* gpxtouch.py l*.gpx

Benchmark:

484 files (279.0 MB) took 451 seconds

