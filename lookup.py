

def term_lookup(term):
    terms=dict()

    terms['http://purl.obolibrary.org/obo/ARG_2000028'] = 'http://purl.obolibrary.org/obo/ARG_2000028' + ' (has vcard)'
    terms['http://purl.obolibrary.org/obo/ARG_2000029'] = 'http://purl.obolibrary.org/obo/ARG_2000029' + ' (vcard of)'
    terms['http://purl.obolibrary.org/obo/BFO_0000001'] = 'http://purl.obolibrary.org/obo/BFO_0000001' + ' (entity)'
    terms['http://purl.obolibrary.org/obo/BFO_0000002'] = 'http://purl.obolibrary.org/obo/BFO_0000002' + ' (continuant)'
    terms['http://purl.obolibrary.org/obo/BFO_0000004'] = 'http://purl.obolibrary.org/obo/BFO_0000004' + ' (independent continuant)'
    terms['http://purl.obolibrary.org/obo/BFO_0000006'] = 'http://purl.obolibrary.org/obo/BFO_0000006' + ' (spatial region)'
    terms['http://purl.obolibrary.org/obo/BFO_0000020'] = 'http://purl.obolibrary.org/obo/BFO_0000020' + ' (specifically dependent continuant)'
    terms['http://purl.obolibrary.org/obo/BFO_0000031'] = 'http://purl.obolibrary.org/obo/BFO_0000031' + ' (generically dependent continuant)'
    terms['http://purl.obolibrary.org/obo/BFO_0000054'] = 'http://purl.obolibrary.org/obo/BFO_0000054' + ' (realized in)'
    terms['http://purl.obolibrary.org/obo/BFO_0000141'] = 'http://purl.obolibrary.org/obo/BFO_0000141' + ' (immaterial entity)'
    terms['http://purl.obolibrary.org/obo/IAO_0000030'] = 'http://purl.obolibrary.org/obo/IAO_0000030' + ' (information content entity)'
    terms['http://purl.obolibrary.org/obo/RO_0000053'] = 'http://purl.obolibrary.org/obo/RO_0000053' + ' (bearer of)'


    try:
        return(terms[term])
    except KeyError:
        return term
    
from rdflib import Namespace
    
VIVO = Namespace("http://vivoweb.org/ontology/core#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
OBO = Namespace("http://purl.obolibrary.org/obo/")
UFL = Namespace("http://vivo.ufl.edu/ontology/vivo-ufl/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
M3C = Namespace("http://www.metabolomics.info/ontologies/2019/metabolomics-consortium#")