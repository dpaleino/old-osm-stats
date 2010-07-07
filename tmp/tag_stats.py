#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

# 23:46 <Federico2> from collections import defaultdict as dd
# 23:46 <Federico2> d = dd(lambda: dd(lambda: 0))
# 23:46 <Federico2> for cot in d.keys():
# 23:46 <Federico2>     for cat, dog in d[cot].items():
# 23:46 <Federico2>         print cot, cat, dog
# 23:46 <Federico2>         
# 23:47 <hanska> eheh grazie :)
# 23:47 <hanska> io ormai non ragiono più..
# 23:47 <hanska> figurati che faccio fatica a tener gli occhi aperti
# 23:47 <Federico2> d[3][4]=5
# 23:47 <Federico2> d[6][7]=8
# 23:47 <Federico2> for cot in d.keys():
# 23:47 <Federico2>     for cat, dog in d[cot].items():
# 23:47 <Federico2>         print cot, cat, dog
# dict([[a] + b.items() for a,b in d.items()])

import psyco
from json import JsonReader, JsonWriter, ReadException

psyco.full()

saved = {}

features = {
	"highway" : [
		("motorway", ""),
		("motorway_link", ""),
		("trunk", ""),
		("trunk_link", ""),
		("primary", ""),
		("primary_link", ""),
		("secondary", ""),
		("secondary_link", ""),
		("tertiary", ""),
		("unclassified", ""),
		("road", ""),
		("residential", ""),
		("living_street", ""),
		("service", ""),
		("track", ""),
		("pedestrian", ""),
		("services", ""),
		("bus_guideway", ""),
		("path", ""),
		("cycleway", ""),
		("footway", ""),
		("bridleway", ""),
		("byway", ""),
		("steps", "Scalinata"),
		("mini_roundabout", ""),
		("stop", "Stop"),
		("traffic_signals", "Semaforo"),
		("crossing", "Strisce pedonali"),
		("incline", ""),
		("incline_steep", ""),
		("ford", "Guado"),
		("bus_stop", "Fermata autobus"),
		("turning_circle", "Slargo per inversione"),
		("construction", "Strada in costruzione"),
		("emergency_access_point", ""),
		("motorway_junction", "Uscita svincolo autostradale/altro"),
	],
	"traffic_calming": [
		("bump", "Dosso artificiale"),
		("chicane", ""),
		("cushion", ""),
		("hump", ""),
		("rumble_strip", ""),
		("table", ""),
		("choker", ""),
	],
	#"service" : [],
	"barrier" : [
		("hedge", "Siepe"),
		("fence", "Recinto"),
		("wall", "Muro"),
		("ditch", ""),
		("retaining_wall", ""),
		("city_wall", "Mura cittadine"),
		("bollard", ""),
		("cycle_barrier", ""),
		("cattle_grid", ""),
		("toll_booth", "Casello"),
		("entrance", "Ingresso"),
		("gate", "Cancello"),
		("stile", ""),
		("sally_port", ""),
	],
	"waterway" : [
		("stream", ""),
		("river", ""),
		("riverbank", ""),
		("canal", ""),
		("drain", ""),
		("dock", ""),
		("lock_gate", ""),
		("turning_point", ""),
		("boatyard", ""),
		("weir", ""),
		("dam", "Diga"),
	],
	"railway" : [
		("rail", "Binario ferroviario"),
		("tram", "Binario tramviario"),
		("light_rail", "Ferrovia leggera"),
		("subway", "Metropolitana"),
		("narrow_gauge", "Ferrovia a scartamento ridotto"),
		("station", "Stazione ferroviaria"),
		("construction", "Ferrovia in costruzione"),
		("monorail", "Monorotaia"),
		("funicular", "Funicolare"),
		("halt", "Fermata ferroviaria"),
		("tram_stop", "Fermata tramviaria"),
		("crossing", "Attraversamento ferroviario pedonale"),
		("level_crossing", "Passaggio a livello"),
		("subway_entrance", "Ingresso metropolitana"),
		("turntable", ""),
		("platform", "Piattaforma ai binari"),
	],
	"aeroway" : [
		("aerodrome", "Aeroporto"),
		("terminal", "Terminal aeroportuale"),
		("helipad", "Eliporto"),
		("runway", "Pista di decollo e atterraggio"),
		("taxiway", "Pista di rullaggio"),
		("apron", ""),
		("gate", "Uscita da terminal"),
		("windsock", ""),
	],
	"aerialway" : [
		("cable_car", "Funivia"),
		("gondola", ""),
		("chair_lift", "Seggiovia"),
		("drag_lift", ""),
		("station", ""),
	],
	#"power" : [],
	"man_made" : [
		("beacon", ""),
		("crane", ""),
		("gasometer", ""),
		("lighthouse", ""),
		("pier", ""),
		("pipeline", ""),
		("reservoir_covered", ""),
		("survellaince", ""),
		("survey_point", ""),
		("tower", ""),
		("wastewater_plant", ""),
		("watermill", ""),
		("water_tower", ""),
		("water_works", ""),
		("windmill", "Mulino a vento"),
		("works", ""),
	],
	"leisure" : [
		("sports_centre", ""),
		("golf_course", ""),
		("stadium", "Stadio"),
		("track", "Pista"),
		("pitch", ""),
		("water_park", ""),
		("marina", ""),
		("slipway", ""),
		("fishing", ""),
		("nature_reserve", "Riserva naturale"),
		("park", "Parco"),
		("playground", ""),
		("garden", "Giardino"),
		("common", ""),
		("ice_rink", ""),
		("miniature_golf", ""),
	],
	"amenity" : [
		("arts_centre", ""),
		("atm", ""),
		("baby_hatch", ""),
		("bank", "Banca"),
		("bbq", "Barbecue"),
		("bench", "Panchina"),
		("biergarten", ""),
		("bicycle_parking", "Parcheggio biciclette"),
		("bicycle_rental", "Noleggio biciclette"),
		("bureau_de_change", "Ufficio di cambio"),
		("bus_station", "Stazione autobus"),
		("brothel", ""),
		("cafe", ""),
		("car_rental", "Noleggio auto"),
		("car_sharing", ""),
		("cinema", "Cinema"),
		("courthouse", "Tribunale"),
		("crematorium", ""),
		("dentist", "Dentista"),
		("doctors", "Medico"),
		("drinking_water", ""),
		("embassy", "Ambasciata"),
		("emergency_phone", "Telefono d'emergenza"),
		("fast_food", ""),
		("ferry_terminal", ""),
		("fire_station", ""),
		("food_court", ""),
		("fountain", "Fontana"),
		("fuel", "Stazione di rifornimento"),
		("grave_yard", "Cimitero"),
		("grit_bin", ""),
		("hospital", "Ospedale"),
		("hunting_stand", ""),
		("kindergarten", ""),
		("library", "Biblioteca"),
		("marketplace", ""),
		("nightclub", "Locale notturno"),
		("parking", "Parcheggio"),
		("pharmacy", "Farmacia"),
		("place_of_worship", "Luogo di culto"),
		("police", "Polizia"),
		("post_box", "Cassetta postale"),
		("post_office", "Ufficio postale"),
		("prison", "Prigione"),
		("pub", "Pub"),
		("public_building", "Edificio pubblico"),
		("recycling", "Punto di riciclaggio"),
		("restaurant", "Ristorante"),
		("school", "Scuola"),
		("shelter", "Tettoia"),
		("signpost", ""),
		("studio", ""),
		("taxi", ""),
		("telephone", "Telefono pubblico"),
		("theatre", "Teatro"),
		("toilets", "Bagno pubblico"),
		("townhall", "Municipio"),
		("university", "Università"),
		("vending_machine", ""),
		("veterinary", "Veterinario"),
		("waste_basket", "Cestino della spazzatura"),
		("waste_disposal", ""),
	],
	"shop" : [
		("alcohol", ""),
		("bakery", "Panificio"),
		("beverages", ""),
		("bicycle", ""),
		("books", "Libreria"),
		("butcher", "Macelleria"),
		("car", "Rivenditore auto"),
		("car_repair", "Autofficina"),
		("chemist", ""),
		("clothes", "Negozio d'abbigliamento"),
		("computer", "Negozio d'informatica"),
		("confectionery", ""),
		("convenience", ""),
		("department_store", ""),
		("dry_cleaning", ""),
		("doityourself", ""),
		("electronics", "Negozio d'elettronica"),
		("florist", "Fioraio"),
		("garden_centre", ""),
		("greengrocer", "Drogheria"),
		("hairdresser", "Parrucchieria"),
		("hardware", "Ferramenta"),
		("hifi", ""),
		("kiosk", "Edicola"),
		("laundry", "Lavanderia"),
		("mall", "Centro commerciale"),
		("motorcycle", ""),
		("optician", "Ottica"),
		("organic", ""),
		("outdoor", ""),
		("sports", "Negozio sportivo"),
		("stationery", ""),
		("supermarket", "Supermercato"),
		("shoes", "Negozio di scarpe"),
		("toys", "Negozio di giocattoli"),
		("travel_agency", "Agenzia di viaggio"),
		("video", "Videoteca"),
	],
	"tourism" : [
		("alpine_hut", ""),
		("attraction", "Attrazione turistica"),
		("artwork", ""),
		("camp_site", ""),
		("caravan_site", ""),
		("chalet", "Chalet"),
		("guest_house", "Pensione"),
		("hostel", "Ostello"),
		("hotel", "Hotel"),
		("information", "Punto informazioni"),
		("motel", "Motel"),
		("museum", "Museo"),
		("picnic_site", ""),
		("theme_park", "Parco tematico"),
		("viewpoint", "Belvedere"),
		("zoo", "Zoo"),
	],
	"historic" : [
		("archaelogical_site", "Sito archeologico"),
		("battlefield", "Campo di battaglia"),
		("castle", "Castello"),
		("memorial", "Memoriale"),
		("monument", "Monumento"),
		("ruins", "Rovine"),
		("wreck", "Relitto"),
	],
	#"landuse" : [],
	#"military" : [],
	#"natural" : [],
	"route" : [
		("bicycle", ""),
		("bus", ""),
		("detour", ""),
		("ferry", ""),
		("flight", ""),
		("hiking", ""),
		("mtb", ""),
		("pub_crawl", ""),
		("road", ""),
		("ski", ""),
		("subsea", ""),
		("tour", ""),
		("tram", ""),
	],
	#"sport" : [],
	#"abutters" : [],
}

def main():
	from optparse import OptionParser
	import os

	global saved

	parser = OptionParser()
	parser.add_option("--planet", dest="planet", action="store",
	                  default=None, help="The planet file to parse")
	parser.add_option("--key", dest="key", action="store",
	                  default=None, help="The key to generate statistics for")
	parser.add_option("--tag", dest="tag", action="store",
	                  default=None, help="The tag to generate statistics for")
	(options, args) = parser.parse_args()

	if not options.planet:
		parser.error("The --planet option is required.")

	if options.key and options.tag:
		parser.error("You cannot specify both --tag and --key.")

	if not options.key and not options.tag:
		parser.error("You must specify one between --tag and --key.")

	if options.key:
		options.tag = "%s=*" % options.key

	try:
		f = open(os.path.expanduser("~/.osmitstats"), "r")
		j = JsonReader()
		saved = j.read(f.readline())
		f.close()
	except ReadException:
		pass

	saved["tagstats"] = {
		"20090617" : parse(options.planet, options.tag)
	}

	print repr(saved)

	f = open(os.path.expanduser("~/.osmitstats"), "w")
	j = JsonWriter()
	f.write(j.write(saved))
	f.close()

def parse(file, tag):
	import xml.sax

	class tagHandler(xml.sax.handler.ContentHandler):
		def __init__(self, tag):
			from collections import defaultdict
			self.stats = defaultdict(lambda: defaultdict(lambda: 0))
			self.parent = None
			self.key, self.value = tag.split("=")
		def startElement(self, name, attr):
			name = name.encode("ascii")
			if name in ('node', 'way'):
				self.parent = attr
			elif name == 'tag':
				if attr.get("k") == self.key:
					if attr.get("v") == self.value:
						self.stats[tag][self.parent.get('user')] += 1
					elif self.value == "*":
						self.stats["%s=%s" % (self.key, attr.get("v"))][self.parent.get('user')] += 1

	parser = xml.sax.make_parser()
	handler = tagHandler(tag)
	parser.setContentHandler(handler)
	parser.parse(file)
	return dict(handler.stats)

if __name__ == '__main__':
	main()
