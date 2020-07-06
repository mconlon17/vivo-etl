# vivo-etl
Experiments with RMLMapper and the creation of triples for VIVO

# Extract

Get data from on-line sources such as PubMed, Dimensions, ORCiD.

The result of "getting data" should be to return collections of JSON objects
ready for further processing.

# Transform

RMLMapper can be used to transform collections of JSON objects to VIVO triples.
Only the transform step needs to be concerned with the VIVO ontologies.

Pre-processing might include:

1. URL finding.  Many entities may already exist in the local VIVO.  We want to match
entities to to their existing URLs.

Some pre-processing and post-processing of RMLmapper work may be needed to make 
triples for VIVO.

Post processing might incude:

1. Validation and inference.  Using `robot`, the triples can be augmented with inferred
triples and validated against the ontology for coherence.  For example, a book can 
not have any roles.
1. SHACL for constraint validation -- does the data conform to expectations for the 
site?  For example, a person should have a name.


# Load

Loading triples can be done with TDBLoader from Jena.  Super fast.