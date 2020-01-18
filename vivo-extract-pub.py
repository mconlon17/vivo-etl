#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-pub: given a pmid, generate metadata for the pub:
        - use a request get to entrez to fetch XML
        - create a pub dict

    All options are set via the command line

    TODO: Add Mesh terms, authors, dates
    TODO: allow the perfect routine to print if verbose.  Print the data returned from entrez
"""

import requests
import argparse
import xmltodict
import json

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.1"


def perfect_pub(pmid):
    entrez_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={{pmid}}&retmode=xml'
    url = entrez_url.replace("{{pmid}}", pmid)
    m = xmltodict.parse(requests.get(url).text)
    pub = dict()

    # the attributes in pub are a union of the attributes used by Zotero and those used by CSL for representing journal
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

    # Find the doi as the value associated with the 'pii' key in the list of article ids

    doi = ''
    ai_list = m['PubmedArticleSet']['PubmedArticle']['PubmedData']['ArticleIdList']['ArticleId']

    for e in ai_list:
        if e['@IdType'] == 'pii':
            doi = e['#text']

    if doi != '':
        pub['doi'] = 'https://doi.org/' + doi
    else:
        pub['doi'] = ''

    pub['extra-note'] = ''
    pub['issn'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['ISSN']['#text']
    pub['issue'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
        'Issue']
    pub['journal-abbreviation'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal'][
        'ISOAbbreviation']
    pub['language'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Language']
    pub['library-catalogue'] = ''
    pub['pages'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Pagination']['MedlinePgn']
    pub['journal-title'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['Title']
    pub['rights'] = ''
    pub['series'] = ''
    pub['series-text'] = ''
    pub['series-title'] = ''
    pub['short-title'] = ''
    pub['title'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['ArticleTitle']
    pub['url'] = ''
    pub['Volume'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
        'Volume']

    # the attributes below are pubmed attributes

    pub['pmid'] = pmid
    pub['pmcid'] = ''
    pub['pmcid_url'] = ''
    pub['nihmsid'] = ''
    pub['mesh'] = ''  # repeated for each term

    return pub


def main():
    parser = argparse.ArgumentParser(description="extract pub from Pubmed for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--pmid", dest="pub", required=True, help="a pmid", metavar="PMID", type=perfect_pub)
    args = parser.parse_args()
    print(args.verbose)
    if args.verbose > 0:
        print(json.dumps(args.pub, indent=4))
    return


if __name__ == "__main__":
    main()
