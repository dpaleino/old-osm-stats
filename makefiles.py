#!/usr/bin/env python

from json import JsonReader, JsonWriter

saved = {}

def color(p):
	"""
	Returns a different color (#rrggbb) depending on the percentage
	(0 < p < 1) passed as argument.
	"""
	# Configurable colors
	great = "#00ffff"
	good = "#00ff00"
	medium = "#e6ff00"
	bad = "#ff9966"

	if p >= 0.8:
		return great
	elif p >= 0.6:
		return good
	elif p >= 0.5:
		return medium
	else:
		return bad

def growth(a, b):
	"""Returns the growth in percent from a to b."""
	return (b - a) / a

def percent(a, b):
	"""Returns percentage of a over b."""
	return float(a) / float(b)

def percent_cmp(a, b):
	if a['percent'] < b['percent']:
		return 1
	elif a['percent'] == b['percent']:
		return 0
	else:
		return -1

def plot(xcoords, ycoords, file, style='b-'):
	import matplotlib.pyplot as plt
	import matplotlib.dates as dts
	from datetime import datetime

	plt.plot_date(map(lambda x: dts.date2num(datetime.strptime(x, "%Y%m%d")), xcoords), ycoords, style)
	plt.savefig(file)

def query(q):
	"""Executes the passed query, and returns a parsed tuple."""
	from subprocess import PIPE, Popen
	from tempfile import NamedTemporaryFile

	#try:
	#print q
	f = NamedTemporaryFile()
	#f = open("/tmp/query", "w")
	out = NamedTemporaryFile()
	
	f.write(q)
	f.flush()

	args = ["psql", "-d", "gis", "-o", out.name, "-f", f.name]
	p = Popen(args, stdout=PIPE, stderr=PIPE)
	#print args
	#print p.communicate()[0]
	p.communicate()
	return parse(out)
#	finally:
#		f.close()
#		out.close()

def parse(f):
	"""
	Returns a list containing rows as tuples of data (each value in
	the tuple is a column).
	"""
	# Drop the two-lines header and the final row
	#+(containing "(num rows)")
	list = []
	#f = open("/tmp/tempfile")
	for row in f.readlines()[2:-2]:
		tmp = row.split('|')
		val = [x.strip() for x in tmp]
		if len(val[0]):
			list.append(tuple(val))
	return list

def comuni_coperti_per_regione():
	global saved

	q = """SELECT p.nome_reg, count(p.cod_pro), count(p.highw)
	FROM (
		SELECT r.nome_reg, c.cod_pro, c.pro_com, c.geom, c.nome_com, c.pop2001, min(s.cod_reg) AS highw
		FROM it_comuni c
		LEFT JOIN osm_stat_%s s
		ON c.pro_com = s.pro_com, it_prov_name p, it_reg_name r
		WHERE p.cod_pro = c.cod_pro AND p.cod_reg = r.cod_reg
		GROUP BY r.nome_reg, c.cod_pro, c.pro_com, c.geom, c.nome_com, c.pop2001
	) p
	GROUP BY p.nome_reg;"""

	print "Esecuzione query comuni coperti per regione... ",
	data = {"old": query(q % saved["previous"]), "new": query(q % saved["current"])}
	print "fatto."

	lists = {"old":[], "new":[]}
	#for region, total, done in data.values():
	for d in data:
		for tuple in data[d]:
			region, total, done = tuple
			lists[d].append({"region": region, "total": int(total), "done": int(done), "percent": percent(done, total)})

	tmplist = lists["new"]
	lists["new"] = sorted(tmplist, cmp=percent_cmp)

	html = """<table class="sortable" rules="none" frame="void" cellspacing="0" border="0">
	<tr>
		<td rowspan="2" align="left"><strong>Regione</strong></td>
		<td rowspan="2" align="left"><strong>Totale</strong></td>
		<td colspan="2" align="center"><strong>Comuni Coperti</strong></td>
		<td colspan="2" align="center"><strong>Percentuale</strong></td>
	</tr>
	<tr>
		<td align="center"><strong>%s</strong></td>
		<td align="center"><strong>%s</strong></td>
		<td align="center"><strong>%s</strong></td>
		<td align="center"><strong>%s</strong></td>
	</tr>
""" % (saved["previous"], saved["current"], saved["previous"], saved["current"])

	total = 0
	done = {"old":0, "new":0}
	for l in lists["new"]:
		html += """	<tr>
		<td align="left"><strong>%s</strong></td>
		<td align="right">%d</td>
		<td align="right">%d</td>
		<td align="right">%d</td>
		<td align="right">%.2f%%</td>
		<td bgcolor="%s" align="right">%.2f%%</td>
	</tr>
""" % (l["region"], l["total"], lists["old"][lists["new"].index(l)]["done"], l["done"], lists["old"][lists["new"].index(l)]["percent"]*100, color(lists["new"][lists["new"].index(l)]["percent"]), l["percent"]*100)

		print repr(lists)
		#print repr(total)
		total += int(l["total"])
		done["old"] += int(lists["old"][lists["new"].index(l)]["done"])
		done["new"] += int(l["done"])

	html += """	<tr>
		<td align="left"><strong>Totale</strong></td>
		<td align="right"><strong>%d</strong></td>
		<td align="right"><strong>%d</strong></td>
		<td align="right"><strong>%d</strong></td>
		<td align="right"><strong>%.2f%%</strong></td>
		<td align="right"><strong>%.2f%%</strong></td>
	</tr>
""" % (total, done["old"], done["new"], percent(done["old"], total) * 100.0, percent(done["new"], total) * 100.0)
	html += "</table>"

	# save percentages
	if saved.has_key("comuni"):
		saved["comuni"].append((saved["current"], percent(done["new"], total) * 100.0))
	else:
		saved["comuni"] = [(saved["current"], percent(done["new"], total) * 100.0),]

	dates = []
	percs = []
	for date, perc in saved["comuni"]:
		dates.append(date)
		percs.append(perc)
	plot(dates, percs, "comuni-coperti.png")
	return html
		
def main():
	from datetime import date
	import os

	global saved

	f = open(os.path.expanduser("~/.osmitstats"), "r")
	j = JsonReader()
	saved = j.read(f.readline())
	print repr(saved)
	f.close()
	#saved["current"] = str(date.today()).replace('-', '')
	#today = str(date.today()).replace('-', '')
	saved["current"] = "20090531"

	q_regioni = """SELECT c.nome_reg, sum(c.pop2001), sum(length(transform(s.intersection, 3395))) AS highw FROM it_comuni c LEFT JOIN osm_stat_20090531 s ON c.pro_com =s.pro_com GROUP BY c.nome_reg ORDER BY nome_reg;"""
	
	f = open("page.html", "w")
	f.write(comuni_coperti_per_regione())
	f.flush()
	f.close()

	# The script has finished now, touch our helper file
	f = open(os.path.expanduser("~/.osmitstats"), "w")
	j = JsonWriter()
	#saved["previous"] = saved["current"]
	saved["current"] = None
	f.write(j.write(saved))
	f.close()

if __name__ == '__main__':
	main()
