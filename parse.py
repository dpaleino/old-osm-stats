#!/usr/bin/env python
#-*- encoding: utf8 -*-

import libxml2
import sys
from genshi.template import MarkupTemplate
from collections import defaultdict

nodes = defaultdict(int)
ways = defaultdict(int)
relations = defaultdict(int)
tags = defaultdict(lambda : defaultdict(int))
newtags = defaultdict(list)

check = {
          "highway": [ 
                       "bus_stop",
                     ],
          "amenity": [
                       "drinking_water",
                       "pharmacy",
                       "bank",
                       "post_office",
                     ]
        }

user = ""

def processNode(reader):
#    print "%d %d %s %d %s" % (reader.Depth(), reader.NodeType(),
#                              reader.Name(), reader.IsEmptyElement(),
#                              reader.Value())
    global user
    node = reader.Name()
    if reader.NodeType() == 1:
        while reader.MoveToNextAttribute():
            if reader.Name() == "user":
                user = unicode(reader.Value(), "utf-8")
                if node == "node":
                    nodes[user] += 1
                elif node == "way":
                    ways[user] += 1
                elif node == "relation":
                    relations[user] += 1
            else:
                if node == "tag":
                    checktag(reader, user)
                    reader.MoveToNextAttribute()

def checktag(reader, user):
    if reader.Name() == "k" and reader.Value() in check.keys():
        k = reader.Value()
        reader.MoveToNextAttribute()
        if reader.Name() == "v" and reader.Value() in check[k]:
            # we're at the correct tag, update the stats
            tagpair = "%s=%s" % (k, reader.Value())
            tags[tagpair][user] += 1

def streamFile(filename):
    try:
        reader = libxml2.newTextReaderFilename(filename)
    except:
        print "Unable to open %s" % (filename)
        return

    ret = reader.Read()
    while ret == 1:
        processNode(reader)
        ret = reader.Read()

    if ret:
        print "Failed to parse %s" % (filename)

def mysort(d):
    ret = []
    for user in d:
        ret.append([d[user], user])
    ret.sort()
    ret.reverse()
    return enumerate(ret)

def main():
    streamFile(sys.argv[1])

    tmpl = MarkupTemplate(open("statistiche.tmpl"))

    for key in tags:
        newtags[key] = mysort(tags[key])

    stream = tmpl.generate(
                           nodes = mysort(nodes),
                           ways = mysort(ways),
                           relations = mysort(relations),
                           date = '20090905',
                           tags = newtags,
                          )
    print stream.render('xhtml')

if __name__ == '__main__':
    main()
