#!/usr/bin/env python

stats_path = "stats.json"
graphs_path = "graphs/"

def plot(xcoords, ycoords, file, style):
    import matplotlib.pyplot as plt
    import matplotlib.dates as dts
    from datetime import datetime

    plt.plot_date(map(lambda x: dts.date2num(datetime.strptime(x, "%Y%m%d")), xcoords), ycoords, style)
    plt.suptitle(file)
    plt.savefig("%s/%s.png" % (graphs_path, file))
    plt.close()

def main():
    from json import JsonReader, JsonWriter, ReadException
    from datetime import date
    from collections import defaultdict
    import os, sys

    try:
        f = open(os.path.expanduser(stats_path), "r")
        j = JsonReader()
        stats = j.read(f.readline())
        f.close()
    except (ReadException, IOError):
        print "Cannot open JSON stats file %s!" % stats_path
        sys.exit(1)

    xcoords = []
    ynodes, yways, yrelations = ([], [], [])
    tags = defaultdict(list)
    newtags = defaultdict(list)
#    print repr(stats)
    for date in stats:
        xcoords.append(date)
        for name in stats[date]:
            value = stats[date][name]
            if name == "nodes":
                ynodes.append([date,value])
            elif name == "ways":
                yways.append([date,value])
            elif name == "relations":
                yrelations.append([date,value])
            elif name == "tags":
                for tag in value:
                    tags[tag].append([date, value[tag]])

    ynodes = sorted(ynodes)
    yways = sorted(yways)
    yrelations = sorted(yrelations)

    for tag in tags:
        newtags[tag] = zip(*sorted(tags[tag]))
        plot(newtags[tag][0], newtags[tag][1], tag, "bo-")

    plot(zip(*ynodes)[0], zip(*ynodes)[1], "nodes", "bo-")
    plot(zip(*yways)[0], zip(*yways)[1], "ways", "r+-")
    plot(zip(*yrelations)[0], zip(*yrelations)[1], "relations", "g^-")

if __name__ == '__main__':
	main()
