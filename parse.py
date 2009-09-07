#!/usr/bin/env python
#-*- encoding: utf8 -*-

import libxml2
import sys
import os

from genshi.template import MarkupTemplate
from collections import defaultdict
from json import JsonReader, JsonWriter, ReadException
from datetime import date

stats_path = "stats.json"
html_path = "statistiche.html"

check = {
    "highway": [
        "bus_stop",
        ],
    "amenity": [
        "drinking_water",
        "pharmacy",
        "bank",
        "post_office",
        ],
    }

nodes = defaultdict(int)
ways = defaultdict(int)
relations = defaultdict(int)

tags = defaultdict(lambda : defaultdict(int))
enumtags = defaultdict(list)
savetags = defaultdict(list)

today = date.today()
today = "%4d%02d%02d" % (today.year,today.month,today.day)

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

def mysort(d, enum = True):
    ret = []
    for user in d:
        ret.append([d[user], user])
    ret.sort()
    ret.reverse()
    if enum:
	    return enumerate(ret)
    else:
        return ret

def save(nodes, ways, relations, tags):
    try:
        j = JsonReader()
        f = open(os.path.expanduser(stats_path), "r")
        stats = j.read(f.readline())
        f.close()
    except (ReadException, IOError):
        f = open(os.path.expanduser(stats_path), "w")
        f.close()
        stats = {}
        pass

    nodes_count = 0
    ways_count = 0
    relations_count = 0

    # let's count primitives
    for pair in mysort(nodes, False):
        nodes_count += pair[0]
    for pair in mysort(ways, False):
        ways_count += pair[0]
    for pair in mysort(relations, False):
        relations_count += pair[0]

    tags_count = defaultdict(int)
    for tag in tags:
        for pair in tags[tag]:
            tags_count[tag] += pair[0]

    stats[today] = {
        "nodes" : nodes_count,
        "ways" : ways_count,
        "relations" : relations_count,
        "tags" : dict(tags_count),
    }

    f = open(os.path.expanduser(stats_path), "w")
    j = JsonWriter()
    f.write(j.write(stats))
    f.close()

def main():
    streamFile(sys.argv[1])

    tmpl = MarkupTemplate(open("statistiche.tmpl"))

    for key in tags:
        enumtags[key] = mysort(tags[key])
        savetags[key] = mysort(tags[key], False)

    save(nodes, ways, relations, savetags)
    stream = tmpl.generate(
        nodes = mysort(nodes),
        ways = mysort(ways),
        relations = mysort(relations),
        date = today,
        tags = enumtags,
        )

    f = open(html_path, "w")
    f.write(stream.render("xhtml"))
    f.close()

if __name__ == '__main__':
    main()
