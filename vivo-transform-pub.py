#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pub-data-loader: given a pmid, generate VIVO data for the pub:
        - use a request get to entrez to fetch XML
        - create a robot template
        - use robot and template to make terms
        - use robot terms and VIVO ontology to validate the terms

    All options are set via the command line
"""
from typing import Dict, Any, Union

import requests
import argparse
import xmltodict
import json

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.0"


def get_pub(pmid):
    entrez_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={{pmid}}&retmode=xml'
    url = entrez_url.replace("{{pmid}}", pmid)
    m = xmltodict.parse(requests.get(url).text)
    pub = dict()

    # the attributes below are a union of the attributes used by Zotero and those used by CSL for representing journal
    # articles
    pub['abstract'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Abstract']['AbstractText']
    pub['accessDate'] = ''
    pub['archive'] = ''
    pub['archiveLocation'] = ''
    pub['callNumber'] = ''
    pub['creator'] = ''
    pub['author'] = ''  # repeated for each
    pub['contributor'] = ''  # repeated for each
    pub['editor'] = ''  # repeated for each
    pub['reviewedAuthor'] = ''  # repeated for each
    pub['translator'] = ''  # repeated for each
    pub['date-issued'] = ''
    pub['doi'] = ''
    pub['extra-note'] = ''
    pub['issn'] = ''  # journal issn
    pub['issue'] = ''
    pub['journal-abbreviation'] = ''
    pub['language'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Language']
    pub['library-catalogue'] = ''
    pub['pages'] = ''
    pub['journal-title'] = ''  # journal title
    pub['rights'] = ''
    pub['series'] = ''
    pub['series-text'] = ''
    pub['series-title'] = ''
    pub['short-title'] = ''
    pub['title'] = ''
    pub['url'] = ''
    pub['volume'] = ''

    # the attributes below are pubmed attributes

    pub['pmid'] = pmid
    pub['pmcid'] = ''
    pub['pmcid_url'] = ''
    pub['nihmsid'] = ''
    pub['mesh'] = ''  # repeated for each term

    return pub


def main():
    parser = argparse.ArgumentParser(description="PubMed data loader for VIVO")
    parser.add_argument('pmid', help="PubMed ID of the paper whose metadata is to be made for VIVO")
    args = parser.parse_args()
    m = get_pub(args.pmid)
    print(json.dumps(m, indent=4))
    return


if __name__ == "__main__":
    main()
