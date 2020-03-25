#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    reformat_rdf.py: Read RDF from stdout and write to stdout.

    TODO: Add Reformat via input and output parameters
"""
from rdflib import Graph
import sys

g = Graph()
g = g.parse(sys.stdin, format="ttl")
f = open("out.ttl", "w")
print(g.serialize(format="ttl").decode('utf-8'), file=f)
