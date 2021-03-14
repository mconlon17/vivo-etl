#!/bin/bash
echo "Get data from ROR"
wget https://api.ror.org/organizations/https://ror.org/$1 -qO- >$2.json
echo "Convert to Raw RDF"
java -jar ../../JSON2RDF/target/json2rdf-jar-with-dependencies.jar http://my.org# <$2.json | riot --formatted=TURTLE >$2-raw.ttl
echo "Convert to ${3-new} VIVO RDF"
robot query --input $2-raw.ttl --query org-ror-${3-new}.sparql $2.ttl
rm $2-raw.ttl $2.json 