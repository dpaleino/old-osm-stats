#!/usr/bin/env python2.5

from collections import defaultdict

levels = {
    "4": "regioni",
    "6": "province",
    "8": "comuni",
    }

boundaries = defaultdict(lambda: defaultdict(str))

relation_id = 0
relation_level = 0
relation_name = ""

look_for_level = False
look_for_name = False

class ParserTarget(object):
    def __init__(self):
        self.events = []
        self.close_count = 0
    def start(self, tag, attrib):
        global relation_id, relation_level, relation_name
        global look_for_level, look_for_name
        print tag, attrib
        if tag == "relation":
            look_for_level = True
            look_for_name = False
            relation_id = attrib["id"]
        elif tag == "tag":
            if look_for_level and attrib["k"] == "admin_level":
                if attrib["v"] in levels:
                    look_for_level = False
                    look_for_name = True
                    relation_level = attrib["v"]
            if look_for_name and attrib["k"] == "name":
                look_for_name = False
                relation_name = attrib["v"]
                boundaries[levels[relation_level]][relation_name] = relation_id
    def close(self):
        events, self.events = self.events, []
        self.close_count += 1
        return events

def main(filename):
    from lxml import etree

    parser = etree.XMLParser(target = ParserTarget())
    infile = open(filename)
    results = etree.parse(infile, parser)
    print results
    infile.close()
    return

if __name__ == "__main__":
    import sys
    try:
        import psyco
        psyco.log()
        psyco.profile()
    except ImportError:
        pass

    main(sys.argv[1])
