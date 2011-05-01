#!/usr/local/bin/python
#
# Copyright (c) 2011 Very Furry / Martijn van Exel.  All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
gpxtouch.py

Takes one or more GPX XML files as argument and sets the modification
and access times to the timestamp of the most recent trackpoint of 
each GPX file.

Sample usages:
* gpxtouch.py long_walk_long_ago.gpx
* gpxtouch.py l*.gpx
"""


import cElementTree
import sys
import datetime
import time
import isodate
import os

SFX = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
t0 = time.time()
count = 0
size = 0
files = sys.argv[1:]
if os.path.isdir(files[0]):
	print "No dirs please, use wildcards"
	sys.exit()
for file in files:
	if os.path.isfile(os.path.abspath(file)):
		count += 1
		size += os.path.getsize(file)
		print "processing %s ..." % file
		date = None
		try:
			for event, elem in cElementTree.iterparse(file):
				if elem.tag.split("}")[1] == "time":
					if date is None:
						date = isodate.parse_datetime(elem.text)
					else:
						newdate = isodate.parse_datetime(elem.text)
						if newdate > date:
							date = newdate
				elem.clear()
		except SyntaxError:
			print "\tnot valid xml"
			pass
		if date is not None:
			t = time.mktime(date.timetuple())
			os.utime(file, (time.time(), t))
		else:
			print "\tNo <time> node found, GPX empty or not GPX"
	else:
		print "%s is not a file" % file
t1 = time.time()
prettysize = ""
for sfx in SFX:
	size /= 1024
	if size < 1024:
		prettysize = '{0:.1f} {1}'.format(size, sfx)
		break

print "%i files (%s) took %i seconds" % (count, prettysize, t1-t0)