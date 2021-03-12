# vivo-etl
Experiments with data ingest from CSV and JSON to VIVO

# The Approach

We use a simple pipeline approach using standard open source utilities to 
extract, transform, and load data from any source to VIVO.

Ontological 
knowledge needed to produce VIVO RDF is isolated in a single SPARQL CONSTRUCT
query specific to the data source and the version of the VIVO ontologies. The
same pipeline can be used to produce data for the curent VIVO ontologies, or
the new VIVO ontologies.  Only the query has to change.

The approach converts JSON data to VIVO RDF using a simple pipeline:

    JSON -> raw RDF -> VIVO RDF -> VIVO triplestore
    
For CSV and TSV files, first convert them to JSON and then follow the same pipeline.

Notice that nothing here is particularly "VIVO" -- we are just making triples and
loading them to a triple store in accordance with some semantics of our choice.

Using this approach we can convert data from any source to any triple store.

# Utilities

## `csv2json.py`

A utility, `csv2json.py` is provided in this repository to convert CSV and TSV files 
to JSON.

When data comes in the form of TSV or CSV, use the utility `csv2json.py` to convert
it to JSON.  For example, the command line below converts a file called 
`enterprise.tsv` and produces a file `entprise.json`, ready for further processing.

    python3 csv2json.py <enterprise.tsv >enterprise.json

## `wget`

Use the command line tool `wget` to create a JSON file from an API.

## `JSON2RDF`

Use [`JSON2RDF](https://github.com/AtomGraph/JSON2RDF) to convert any JSON file a *raw* RDF file.  `JSON2RDF` uses the 
semantics
of the JSON file to create predicates for the triples it uses to create RDF.

## `robot`

Use [`robot`](http://robot.obolibrary.org/) to convert the raw RDF produced by `JSON2RDF` to VIVO RDF for the
ontologies of choice by using an appropriate SPARQL CONSTRUCT query.  Examples
are provided.

## `tdbloader`

Use [tdbloader](https://jena.apache.org/documentation/tdb/commands.html#tdbloader) for loading triples to a triple store.  It's super fast. And
for MacOS, and Linux, there's [tdbloader2](https://jena.apache.org/documentation/tdb/commands.html#tdbloader2) that's even faster.

# Examples

We hope to build a small library (you can help!) of examples for various sources and
targets.  For VIVO, we have two targets in mind: 1) the existing VIVO ontology and
ontologies used by the VIVO ontology to make data that can be loaded into a current
version of VIVO, and 2) the new VIVO ontologies, to have data ready when the software
is able to use the new ontologies.

Entities | Source | Target | Query VIVO | Query New 
--- | --- | --- | --- | --- 
Organizations | ROR | new VIVO | `org-ror-new.sparql` |`org-ror-new.sparql`