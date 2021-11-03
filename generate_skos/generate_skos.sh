#!/usr/bin/env bash
tarql=./tarql-1.2/bin/tarql 

rm -rf ./dist
mkdir ./dist

./lib/normalize.py data/vak.csv Onderwijsniveau Onderwijsgraad Thema > ./dist/vak.csv
./lib/normalize.py data/thema.csv "Officiële vakkenlijst - koppeling" > ./dist/thema.csv
./lib/normalize.py data/onderwijsniveau.csv Onderwijsgraad > ./dist/onderwijsniveau.csv
./lib/normalize.py data/onderwijsgraad.csv Onderwijsniveau > ./dist/onderwijsgraad.csv

for f in ./lib/*.sparql; do
    $tarql $f > dist/${f/'.sparql'/'.skos.ttl'}
done

ttl-merge -i ./dist -p ./lib/prefixes.json > dist/merged.skos.ttl
