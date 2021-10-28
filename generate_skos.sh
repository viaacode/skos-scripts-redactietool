#!/usr/bin/env bash
tarql=./tarql-1.2/bin/tarql 

mkdir dist

./normalize.py original/vak.csv Onderwijsniveau Onderwijsgraad Thema > ./dist/vak.csv
./normalize.py original/thema.csv "Officiële vakkenlijst - koppeling" > ./dist/thema.csv
./normalize.py original/onderwijsniveau.csv Onderwijsgraad > ./dist/onderwijsniveau.csv
./normalize.py original/onderwijsgraad.csv Onderwijsniveau > ./dist/onderwijsgraad.csv

for f in ./*.sparql; do
    $tarql $f > dist/${f/'.sparql'/'.skos.ttl'}
done

ttl-merge -i ./dist -p ./prefixes.json > dist/merged.skos.ttl
