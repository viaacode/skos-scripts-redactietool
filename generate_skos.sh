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
./resources/collect.py ./data/vak.csv Vak https://w3id.org/onderwijs-vlaanderen/id/collectie/vak --ordered --ns https://w3id.org/onderwijs-vlaanderen/id/vak/ --label "vakken" > ./dist/vak-collection.skos.ttl

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

$tarql -H -e "utf-8" ./resources/onderwijsstructuur.sparql ./data/onderwijsstructuur.csv  > ./dist/onderwijsstructuur.skos.ttl

# Create Collection
./resources/collect.py ./data/onderwijsstructuur.csv Onderwijsniveau https://w3id.org/onderwijs-vlaanderen/id/collectie/niveau --ns https://w3id.org/onderwijs-vlaanderen/id/structuur/ --label "onderwijsniveaus" > ./dist/niveau-collection.skos.ttl
./resources/collect.py ./data/onderwijsstructuur.csv Onderwijssubniveau https://w3id.org/onderwijs-vlaanderen/id/collectie/subniveau --ns https://w3id.org/onderwijs-vlaanderen/id/structuur/ --label "onderwijs subniveaus" > ./dist/subniveau-collection.skos.ttl
# Create OrderedCollection
./resources/collect.py ./data/onderwijsstructuur.csv Onderwijsgraad https://w3id.org/onderwijs-vlaanderen/id/collectie/graad --ordered --ns https://w3id.org/onderwijs-vlaanderen/id/structuur/ --label "onderwijsgraden" > ./dist/graad-collection.skos.ttl
./resources/collect.py ./data/onderwijsstructuur.csv Leerjaar https://w3id.org/onderwijs-vlaanderen/id/collectie/leerjaar --ordered --ns https://w3id.org/onderwijs-vlaanderen/id/structuur/ --label "onderwijs leerjaren" > ./dist/leerjaar-collection.skos.ttl

# merge the files
ttl-merge -i ./dist/onderwijsstructuur.skos.ttl ./dist/niveau-collection.skos.ttl ./dist/subniveau-collection.skos.ttl ./dist/graad-collection.skos.ttl ./dist/leerjaar-collection.skos.ttl -p ./resources/prefixes.json > dist/onderwijsstructuur-merged.skos.ttl
# cleanup
skosify ./dist/onderwijsstructuur-merged.skos.ttl -o ./dist/onderwijsstructuur-final.skos.ttl

# --- Merge all files ---
ttl-merge -i ./dist/*-final.skos.ttl -p ./resources/prefixes.json > ./dist/all.skos.ttl