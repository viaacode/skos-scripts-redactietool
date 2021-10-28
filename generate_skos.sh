#!/usr/bin/env bash
tarql=./tarql-1.2/bin/tarql 

rm -rf ./dist
mkdir ./dist

./normalize.py data/vak.csv Onderwijsniveau Onderwijsgraad Thema > ./dist/vak.csv
./normalize.py data/thema.csv "Officiële vakkenlijst - koppeling" > ./dist/thema.csv
./normalize.py data/onderwijsniveau.csv Onderwijsgraad > ./dist/onderwijsniveau.csv
./normalize.py data/onderwijsgraad.csv Onderwijsniveau > ./dist/onderwijsgraad.csv

for f in ./*.sparql; do
    $tarql $f > dist/${f/'.sparql'/'.skos.ttl'}
done

ttl-merge -i ./dist -p ./prefixes.json > dist/merged.skos.ttl
