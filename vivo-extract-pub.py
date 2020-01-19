#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-pub: given a pmid, generate metadata for the pub:
        - use a request get to entrez to fetch XML
        - create a pub dict

    All options are set via the command line

    TODO: Add Mesh terms, authors
"""

import requests
import argparse
import xmltodict
import json

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.1"

args = None


def make_author_list(a_list):

    # from a list of authors, return a string of the the author names

    authors = ''
    n_authors = len(a_list)
    for a in a_list:
        authors += a["LastName"] + ', ' + a["ForeName"]
        if a != a_list[n_authors-1]:
            authors += ', '
    return authors


def make_date(date_dict):

    # from a date_dict, make a single string date value

    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    return date_dict["Year"] + months[date_dict["Month"]] + date_dict["Day"]


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
    pub['date-issued'] = make_date(
        m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
            'PubDate'])

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
    pub['keywords'] = make_keywords(m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['KeywordList']['Keyword'])

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
    return


if __name__ == "__main__":
    main()
