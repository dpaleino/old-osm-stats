#!/bin/bash

url="http://download.geofabrik.de/osm/europe/italy.osm.bz2"
today=$(date +%Y%m%d)
output="italy_$today.osm"
prefix="italy_$today"

[ -d ../archive ] || mkdir ../archive/
wget $url -O ../archive/$output.bz2

# Import data into PostGIS
osm2pgsql -l -p $prefix ../archive/$output.bz2

# Create the statistics table
echo "CREATE TABLE osm_stat_$today AS \
SELECT c.cod_reg, c.pro_com, l.highway, l.ref, l.name, intersection(l.way, transform(c.geom, 4326)) \
FROM $prefix_line l, it_comuni c \
WHERE l.highway <> '' AND l.way &&  transform(c.geom, 4326) AND intersects(l.way, transform(c.geom, 4326))" | \
	psql -d gis

if [ "$?" -eq 2 ]; then
	mail --subject "Statistics table creation failed!" d.paleino+osmit@gmail.com
fi
