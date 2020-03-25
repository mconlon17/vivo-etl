#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    improve_rdf.py: Read RDF from RMLMapper.  Make a few improvements:

    1. Remove triples with empty text values ("")
    2. Remove triples with subject or object URI that end with "/" -- these result when RMLMapper template has two values
       and the second one is null.  In such cases, a subject should not be generated
"""
from rdflib import Graph
import sys
from rdflib import Namespace


input_g = Graph()
input_g = input_g.parse(sys.stdin, format="ttl")
error_g = Graph()
for s, p, o in input_g:
    print(s, p, o)
    if str(s).endswith("/"):
        error_g.add((s, p, o))
    elif str(o).endswith("/"):
        error_g.add((s, p, o))
    elif str(o) == "":
        error_g.add((s, p, o))

output_g = input_g - error_g
output_g.bind('foaf', "http://xmlns.com/foaf/0.1/")
output_g.bind('data', 'http://vivo.ufl.edu/individual/')
output_g.bind('', 'http://vivoweb.org/ontology/core#')
output_g.bind('vcard', 'http://www.w3.org/2006/vcard/ns#')
output_g.bind('uf', 'http://vivo.ufl.edu/ontology/vivo-ufl/')
output_g.bind('obo', 'http://purl.obolibrary.org/obo/')


f = open("out.ttl", "w")
print(output_g.serialize(format="ttl").decode('utf-8'), file=f)
