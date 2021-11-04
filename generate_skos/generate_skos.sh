#!/usr/bin/env bash
tarql=./tarql-1.2/bin/tarql 

rm -rf ./dist
mkdir ./dist

./resources/normalize.py data/vak.csv Onderwijsniveau Onderwijsgraad Thema > ./dist/vak.csv
./resources/normalize.py data/thema.csv "Officiële vakkenlijst - koppeling" > ./dist/thema.csv
./resources/normalize.py data/onderwijsniveau.csv Onderwijsgraad > ./dist/onderwijsniveau.csv
./resources/normalize.py data/onderwijsgraad.csv Onderwijsniveau > ./dist/onderwijsgraad.csv

for f in ./resources/*.sparql; do
    filename="${f##*/}"
    csvfile=dist/${filename/'.sparql'/'.csv'}

    out=dist/${filename/'.sparql'/'.skos.ttl'}

    $tarql -H -e "utf-8" $f $csvfile  > $out
done

ttl-merge -i ./dist -p ./resources/prefixes.json > dist/merged.skos.ttl
skosify ./dist/merged.skos.ttl -o ./dist/final.skos.ttl