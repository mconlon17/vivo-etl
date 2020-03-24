#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-mesh-term: from MeSH, return a term object
"""

import argparse
import requests
import json

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.1"

args = None


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
        raise argparse.ArgumentError(val + ' an unknown date')
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


def main():
    global args

    parser = argparse.ArgumentParser(description="extract term for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--term", dest="term", required=True,
                        help="the name of term to be extracted", metavar="TERM",
                        type=str)
    args = parser.parse_args()
    if args.verbose > 0:
        print(args.term)

    term = perfect_term(args.term)

    print(term)
    return

if __name__ == "__main__":
    main()
