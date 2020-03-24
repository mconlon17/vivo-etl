#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-pub: given a pmid, generate metadata for the pub:
        - use a request get to entrez to fetch XML
        - create a pub dict

    All options are set via the command line

    TODO: Add people objects
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


def perfect_journal(issn, title, isoabbrev):
    from datetime import datetime

    m = dict(kind='journal')
    m['extract_date'] = perfect_date(datetime.today().strftime('%Y%m%d'))

    m['issn'] = issn
    m['title'] = title
    m['iso-abbreviation'] = isoabbrev

    return m


def perfect_grant(identifier, grantor, country, date):
    from datetime import datetime

    m = dict(kind='grant')
    m['extract_date'] = perfect_date(datetime.today().strftime('%Y%m%d'))

    m['identifier'] = identifier
    m['grantor'] = grantor
    m['country'] = country
    if date != '':
        m['award-date'] = perfect_date(date)
    return m


def perfect_term(val):
    from datetime import datetime
    global args

    # Given the text descriptor of a potential MeSH term, use the MeSH API to get metadata for the term

    m = dict(kind='term')
    val = val.replace("'", "")
    val = val.replace('"', '')
    m['name'] = val

    mesh_api_url = 'https://id.nlm.nih.gov/mesh/lookup/descriptor?label={{val}}&match=exact&limit=10'
    url = mesh_api_url.replace("{{val}}", val)
    request = requests.get(url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}).json()
    print(request)
    if args.verbose > 1:
        print(json.dumps(request, indent=4))
    m['resource_url'] = request[0]['resource']
    m['rdf_url'] = m['resource_url'] + '.rdf'
    m['identifier'] = m['resource_url'][27:]  # The resource URL ends with identifier
    m['vocabulary'] = 'mesh'
    m['extract_date'] = perfect_date(datetime.today().strftime('%Y%m%d'))
    return m


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


def perfect_date(val):
    from datetime import datetime
    m = dict(kind='date')
    val = val.replace('-', '')
    val = val.replace('/', '')
    if len(val) == 4:
        m['date'] = val + '0101'
        m['precision'] = 'year'
    elif len(val) == 6:
        m['date'] = val + '01'
        m['precision'] = 'month'
    elif len(val) == 8:
        m['date'] = val
        m['precision'] = 'day'
    else:
        print("in Perfect_date", val)
        raise argparse.ArgumentError(val + ' an unknown date')
    return m


def make_date(date_dict):

    # from a date_dict, make a single string date value

    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    return date_dict["Year"] + date_dict['Month'] if date_dict["Month"].startswith('0') or date_dict[
        "Month"].startswith('1') else months[date_dict["Month"]] + date_dict["Day"]


def make_journal(journal_thing):

    # Given a PubMed journal_thing, find the values to feed to perfect_journal and return its value

    return perfect_journal(journal_thing['ISSN']['#text'], journal_thing['Title'], journal_thing['ISOAbbreviation'])


def make_grants(grant_list):

    # Given a pubmed term list, return extracted terms

    return_list = []

    for grant in grant_list:
        d = perfect_grant(grant['GrantID'], grant['Agency'], grant['Country'], '')
        return_list.append(d)

    return return_list


def make_terms(terms_list):

    # Given a pubmed term list, return extracted terms

    return_list = []

    for term in terms_list:
        d = perfect_term(term['DescriptorName']["#text"])
        return_list.append(d)

    return return_list


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
    pub['date-issued'] = perfect_date(make_date(
        m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
            'PubDate']))

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

    try:
        pub['Volume'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal']['JournalIssue'][
            'Index']
    except KeyError:
        pub['Index'] = ''

    pub['language'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Language']
    pub['library-catalogue'] = ''

    try:
        pub['pages'] = m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Pagination']['MedlinePgn']
    except KeyError:
        pub['pages'] = ''

    try:
        pub['journal'] = make_journal(
            m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Journal'])
    except KeyError:
        pub['journal'] = ''

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

    # MeSH terms

    try:
        pub['terms'] = make_terms(
            m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['MeshHeadingList']['MeshHeading'])
    except KeyError:
        pub['terms'] = ''

    # Grant references

    try:
        pub['grants'] = make_grants(
            m['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['GrantList']['Grant'])
    except KeyError:
        pub['grants'] = ''

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
