#!/usr/bin/env python

import sys
from lxml import etree

class NodeTarget(object):
	def __init__(self):
		self.uid = 0
		self.user = ""
		self.osmid = 0
		self.tuple = (self.osmid, self.uid, self.user)

	def start(self, tag, attrib):
		if tag == 'node':
			self.uid = attrib["uid"]
			self.user = attrib["user"]
			self.osmid = attrib["id"]

	def end(self, tag):
		pass

	def data(self, data):
		pass

	def close(self):
		return self.tuple

infile = sys.argv[1]

users = {}
context = etree.iterparse(infile, tag='node')
for event, elem in context:
	try:
		uid = elem.attrib["uid"]
		if users.has_key(elem.attrib["uid"]):
			users[elem.attrib["uid"]]["features"].append(elem.attrib["id"])
		else:
			users[elem.attrib["uid"]] = {"name": elem.attrib["user"], "features": [elem.attrib["id"]]}
		elem.clear()
		while elem.getprevious() is not None:
			del elem.getparent()[0]
	except KeyError:
		continue

print repr(users)
