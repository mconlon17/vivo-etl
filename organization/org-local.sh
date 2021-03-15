#!/bin/bash
echo "Convert local tsv data to JSON"
python3 ../csv2json.py <$1.tsv >$1.json
echo "Convert to Raw RDF"
java -jar ../../JSON2RDF/target/json2rdf-jar-with-dependencies.jar http://my.org# <$1.json | riot --formatted=TURTLE >$1-raw.ttl
echo "Convert to ${2-new} VIVO RDF"
robot query --input $1-raw.ttl --query org-local-${2-new}.sparql $1.ttl
# rm $1-raw.ttl $1.json 