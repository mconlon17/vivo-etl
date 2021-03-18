# vivo-etl
Experiments with data ingest from CSV and JSON to current VIVO and to the new VIVO 
ontologies.

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
    
For CSV and TSV files, first convert them to JSON using csv2json (see below) and then 
follow the same pipeline.

Notice that nothing here is particularly "VIVO" -- we are just making triples and
loading them to a triple store in accordance with some semantics of our choice.

Using this approach we can convert data from any source to any triple store.

URLs for entities are constructed from PIDS.


# Examples

We hope to build a small library (you can help!) of examples for various sources and
targets.  For VIVO, we have two targets in mind: 1) the existing VIVO ontology and
ontologies used by the VIVO ontology to make data that can be loaded into a current
version of VIVO, and 2) the new VIVO ontologies, to have data ready when the software
is able to use the new ontologies.

| Entities | Source | Script | Example |
| --- | --- | --- | --- | 
|Organization | ROR | ./org-ror.sh *rorid* *outfile* [vivo\|new] | ./org-ror.sh 02y3ad647 uf new |
| | Local | ./org-local.sh *filename*  [vivo\|new] | ./org-local.sh org-local new| 
|Publication | Pubmed |  |  |
|  | CrossRef | | |
| | Local | | |
|  | Figshare | | |
|Dataset | DataCite | | |
|  | Local | | |
|Person | ORCID | | Need API Key|
|  | Local | | |
|Project | Local | | |
|Resource | Local | | |
