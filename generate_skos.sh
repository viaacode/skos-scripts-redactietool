#!/usr/bin/env bash
tarql=./tarql-1.2/bin/tarql 

rm -rf ./dist
mkdir ./dist

# --- Vakken ---

# Normalize and map data
./resources/normalize.py ./data/vak.csv Onderwijsniveau Onderwijsgraad Thema > ./dist/vak-normalized.csv
$tarql -H -e "utf-8" ./resources/vak.sparql ./dist/vak-normalized.csv  > ./dist/vak.skos.ttl
$tarql -H -e "utf-8" ./resources/vak-related.sparql ./dist/vak-normalized.csv  > ./dist/vak-related.skos.ttl

# Create OrderedCollection
./resources/collect.py ./data/vak.csv Vak https://data.hetarchief.be/id/onderwijs/collectie/vak --ordered --ns https://data.hetarchief.be/id/onderwijs/vak/ --label "vakken" > ./dist/vak-collection.skos.ttl

# merge the files
ttl-merge -i ./dist/vak.skos.ttl ./dist/vak-collection.skos.ttl -p ./resources/prefixes.json > ./dist/vak-norelated-merged.skos.ttl
ttl-merge -i ./dist/vak.skos.ttl ./dist/vak-collection.skos.ttl ./dist/vak-related.skos.ttl -p ./resources/prefixes.json > ./dist/vak-merged.skos.ttl

# cleanup
skosify ./dist/vak-merged.skos.ttl -o ./dist/vak-final.skos.ttl
skosify ./dist/vak-norelated-merged.skos.ttl -o ./dist/vak-norelated-final.skos.ttl

# --- Themas ---
# Normalize and map data
./resources/normalize.py data/thema.csv "Officiële vakkenlijst - koppeling" > ./dist/thema-normalized.csv
$tarql -H -e "utf-8" ./resources/thema.sparql ./dist/thema-normalized.csv  > ./dist/thema.skos.ttl

# Create OrderedCollection
./resources/collect.py ./data/thema.csv Thema https://data.hetarchief.be/id/onderwijs/collectie/thema --ordered --ns https://data.hetarchief.be/id/onderwijs/thema/ --label "themas" > ./dist/thema-collection.skos.ttl

# merge the files
ttl-merge -i ./dist/thema.skos.ttl ./dist/thema-collection.skos.ttl -p ./resources/prefixes.json > ./dist/thema-merged.skos.ttl

# cleanup
skosify ./dist/thema-merged.skos.ttl -o ./dist/thema-final.skos.ttl


# --- Onderwijsstructuur ---

# -> old data <-
# ./resources/normalize.py data/onderwijsniveau.csv Onderwijsgraad > ./dist/onderwijsniveau.csv
# $tarql -H -e "utf-8" ./dist/onderwijsniveau.sparql ./dist/onderwijsniveau.csv  > ./dist/onderwijsniveau.skos.ttl

# ./resources/normalize.py data/onderwijsgraad.csv Onderwijsniveau > ./dist/onderwijsgraad.csv
# $tarql -H -e "utf-8" ./dist/onderwijsgraad.sparql ./dist/onderwijsgraad.csv  > ./dist/onderwijsgraad.skos.ttl

# ttl-merge -i ./dist/onderwijsgraad.skos.ttl ./dist/onderwijsniveau.skos.ttl -p ./resources/prefixes.json > dist/onderwijsstructuur.skos.ttl
# skosify ./dist/onderwijsstructuur.skos.ttl -o ./dist/onderwijsstructuur-final.skos.ttl 

$tarql -H -e "utf-8" ./resources/onderwijsstructuur.sparql ./data/onderwijsstructuur.csv  > ./dist/onderwijsstructuur.skos.ttl

# Create Collection
./resources/collect.py ./data/onderwijsstructuur.csv Onderwijsniveau https://data.hetarchief.be/id/onderwijs/collectie/niveau --ns https://data.hetarchief.be/id/onderwijs/structuur/ --label "onderwijsniveaus" > ./dist/niveau-collection.skos.ttl
./resources/collect.py ./data/onderwijsstructuur.csv Onderwijssubniveau https://data.hetarchief.be/id/onderwijs/collectie/subniveau --ns https://data.hetarchief.be/id/onderwijs/structuur/ --label "onderwijs subniveaus" > ./dist/subniveau-collection.skos.ttl
# Create OrderedCollection
./resources/collect.py ./data/onderwijsstructuur.csv Onderwijsgraad https://data.hetarchief.be/id/onderwijs/collectie/graad --ordered --ns https://data.hetarchief.be/id/onderwijs/structuur/ --label "onderwijsgraden" > ./dist/graad-collection.skos.ttl
./resources/collect.py ./data/onderwijsstructuur.csv Leerjaar https://data.hetarchief.be/id/onderwijs/collectie/leerjaar --ordered --ns https://data.hetarchief.be/id/onderwijs/structuur/ --label "onderwijs leerjaren" > ./dist/leerjaar-collection.skos.ttl

# merge the files
ttl-merge -i ./dist/onderwijsstructuur.skos.ttl ./dist/niveau-collection.skos.ttl ./dist/subniveau-collection.skos.ttl ./dist/graad-collection.skos.ttl ./dist/leerjaar-collection.skos.ttl -p ./resources/prefixes.json > dist/onderwijsstructuur-merged.skos.ttl
# cleanup
skosify ./dist/onderwijsstructuur-merged.skos.ttl -o ./dist/onderwijsstructuur-final.skos.ttl

# --- Merge all files ---
ttl-merge -i ./dist/*-final.skos.ttl -p ./resources/prefixes.json > ./dist/all.skos.ttl