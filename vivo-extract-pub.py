#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-pub: given a pmid, generate metadata for the pub:
        - use a request get to entrez to fetch XML
        - create a pub dict

    All options are set via the command line

    TODO: Add Mesh term objects, people objects, grant objects, journal objects
"""

import requests
import argparse
import xmltodict
import json
from datetime import datetime

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.1"

args = None


def make_abstract(abstract_thing):

    # PubMed abstract entry, return abstract entry if possible

    abstract = ''
    if 'CopyrightInformation' in abstract_thing:
        return ''  # Do not return copyrighted abstract information
    if 'AbstractText' in abstract_thing:
        abt = abstract_thing['AbstractText']
        if isinstance(abt, str):
            return abt
        elif isinstance(abt, list):
            for a in abt:
                abstract += a["@Label"]
                abstract += ': '
                abstract += a["#text"]
                abstract += ' '

    return abstract


def make_author_list(a_list):

    # from a list of authors, return a string of the the author names

    authors = ''
    n_authors = len(a_list)
    for a in a_list:
        try:
            authors += a["LastName"] + ', ' + a["ForeName"]
        except KeyError:
            try:
                authors += a["CollectiveName"]
            except KeyError:
                continue  # No first name, last name and no collective name, so no author in author list
        if a != a_list[n_authors-1]:
            authors += ', '
    return authors


def make_date(date_dict):

    # from a date_dict, make a single string date value

    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    return str(dict(date=datetime.strptime(date_dict["Year"] + months[date_dict["Month"]] + date_dict["Day"], "%Y%m%d"),
                    precision='day'))


def make_keywords(kw_list):

    # from a kw_list, return the keyword values

    keywords = []

    for keyword_dict in kw_list:
        keywords.append(keyword_dict["#text"])

    return keywords


def perfect_pub(pmid):
    global args

    entrez_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={{pmid}}&retmode=xml'
    url = entrez_url.replace("{{pmid}}", str(pmid))
    m = xmltodict.parse(requests.get(url).text)
    if args.verbose > 1:
        print(json.dumps(m, indent=4))

    pub = dict(kind='pub')

    # the attributes in pub are a union of the attributes used by Zotero and those used by CSL for representing journal
    # articles

    try:
        pub['abstract'] = make_abstract(
            m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Abstract'])
    except KeyError:
        pub['abstract'] = ''

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
    pub['date-issued'] = make_date(
        m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
            'PubDate'])

    # Find the identifiers as the values associated with keys in the list of article ids

    doi = ''
    pmcid = ''
    nihmsid = ''
    ai_list = m['PubmedArticleSet']['PubmedArticle']['PubmedData']['ArticleIdList']['ArticleId']

    for e in ai_list:
        if e['@IdType'] == 'doi':
            doi = e['#text']
        elif e['@IdType'] == 'pmc':
            pmcid = e['#text']
        elif e['@IdType'] == 'mid':
            nihmsid = e['#text']

    if doi != '':
        pub['doi'] = 'https://doi.org/' + doi
    else:
        pub['doi'] = ''

    pub['extra-note'] = ''
    pub['issn'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['ISSN']['#text']

    try:
        pub['Volume'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
            'Index']
    except KeyError:
        pub['Index'] = ''

    pub['journal-abbreviation'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal'][
        'ISOAbbreviation']
    pub['language'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Language']
    pub['library-catalogue'] = ''

    try:
        pub['pages'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Pagination']['MedlinePgn']
    except KeyError:
        pub['pages'] = ''

    pub['journal-title'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['Title']
    pub['rights'] = ''
    pub['series'] = ''
    pub['series-text'] = ''
    pub['series-title'] = ''
    pub['short-title'] = ''
    pub['title'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['ArticleTitle']
    pub['url'] = ''

    try:
        pub['Volume'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
            'Volume']
    except KeyError:
        pub['Volume'] = ''

    # the attributes below are pubmed attributes

    pub['pmid'] = pmid if pmid != '' else ''
    pub['pmcid'] = pmcid if pmcid != '' else ''
    pub['pmcid_url'] = 'http://www.ncbi.nlm.nih.gov/pmc/articles/' + pmcid if pmcid != '' else ''
    pub['nihmsid'] = nihmsid if nihmsid != '' else ''

    try:
        pub['keywords'] = make_keywords(
            m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['KeywordList']['Keyword'])
    except KeyError:
        pub['keywords'] = ''

    # even more attributes

    pub['author_list'] = make_author_list(
        m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['AuthorList']['Author'])

    return pub


def main():
    global args
    parser = argparse.ArgumentParser(description="extract pub from Pubmed for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--pmid", dest="pmid", required=True, help="a pmid", metavar="PMID", type=int)
    args = parser.parse_args()
    print(args.verbose)
    if args.verbose > 0:
        print("Retrieving", args.pmid, "from PubMed")
    pub = perfect_pub(args.pmid)
    if args.verbose > 0:
        print(json.dumps(pub, indent=4))
    print(pub)
    return


if __name__ == "__main__":
    main()
