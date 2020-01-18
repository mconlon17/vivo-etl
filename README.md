# VIVO ETL

[VIVO](https://github.com/vivo-project) uses an ontology to represent scholarship.  VIVO 
collects data from sources local to
the institution (people, personnel positions, awards and honors, teaching, performances, 
advising), and combines these data with data from external sources (papers, books, 
grants), as well as data from external sources that a referred to by all these data 
(journals, locations, concepts, dates, organizations).

In each case, an "ETL" must be performed -- raw data must be extracted from a source,
transformed to valid VIVO assertions in the VIVO ontology, and loaded into the VIVO
triple store.

## Data Extractor

A data extractor:

    m <- dataextractor(pid)
    
The data extractor knows its source, its domain (person, paper, etc) and returns a set of
key-value pairs (m) containing the metadata extracted from the source.

Data extractors can be quite simple, using an API call to a remote source, reading a row from 
a spreadsheet, making a database call, and returning a simple metadata object for further 
processing.

Data extractors are fragile --  if the source3 changes, the data extractor must change.

## Data translator

A data translator is a pipeline from a persistent identifier (PID) to the VIVO assertions 
needed
to represent a NamedIndividual in VIVO with the PID.

A data translator creates a single validated NamedIndividual.

### Examples

* A pubmed data translator would take a PID and return the paper's metadata as VIVO RDF.
* A person data translator would take an ORCiD and return the person's metadata as 
VIVO RDF.
* A journal data translator would take an ISSN.
* A date data translator would take the date in canonical form (yyyy-mm-dd)

### Data translator pattern

A data translator:

     (uri, assertions) <- datatranslator(m)

The data translator pipeline:

1. The data translator contains business logic that maps the raw metadata to the VIVO 
ontology and produces a robot 
template.  The `map` is fragile.  If the VIVO Ontology changes, the `map` must change.
    * Note: The raw metadata may contain references to other entities with their PIDs.  
    The data
translator uses the appropriate data translator to resolve these references.  For example, 
the
raw metadata for a paper refers to one or more authors (people) and to a journal, and to a
date of publication.  In each case, the appropriate data translator (people, journal, 
date) is used to develop the
metadata for the referent and supply the URI to the parent data translator.
1. robot (an OBO tool) is used to create a NamedIndividual for the entity.
1. robot is used to validate the NamedIndividual against the VIVO ontology.
1. The NamedIndividual and the URI of the NamedIndividual are returned.

Data translators are fragile.  If the ontology chnages, the translator must change.  If the
map changes, the data translator must change.

## Data Loader

A data loader is a pipeline that uses data translators to process collections of PID,
and load the assertions resulting from the data translators to VIVO.  The data loader
is authorized to write data to the VIVO triple store.

A data loader:

    VIVO <- dataloader(assertions)
    
Data loaders are dependent on the VIVO APIs.  If the VIVO APIs change, the data loader must be changed.
