#!/bin/bash
echo "Get PMID data from Pubmed"
wget https://api.test.datacite.org/dois/$1 -qO- >$2.json
echo "Convert to Raw RDF"
java -jar ../JSON2RDF/target/json2rdf-jar-with-dependencies.jar http://my.org# <$2.json | riot --formatted=TURTLE >$2-raw.ttl
echo "Convert to ${3-new} VIVO RDF"
robot query --input $2-raw.ttl --query data-datacite-${3-new}.sparql $2.ttl
rm $2-raw.ttl $2.json 