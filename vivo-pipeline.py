#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-pipeline:  Given a spreadsheet, create VIVO data and load to VIVO.  Do everything responsibly:

    1) Use PythonAnywhere APIs to fetch elements from the "world" that are identified -- MeSH terms, dates, pubmed,
       DOI, etc, etc.  Convert to JSON and build a hierarchical document as needed -- a person may have many papers.
       Support some standard entity spreadsheets-- person, org -- perhaps everything starts with these two.
    2) Transform the JSON to TTL using RMLMapper.
    3) Check the TTL using SHACL constraints.  Add inferred helper properties (authorOf, counts of things)
    4) VIVO IRI rewriting.  Query a VIVO to get good IRIs.  Rewrite the TTL with good IRI.
    5) Robot reasoning and reduce for sound ontological assertions.

    Voila.  VIVO data.

    All options are set via the command line

    Some principles:
    1) Don't over engineer (don't assume, don't limit, don't require, don't force)
    2) Show the human where the error(s) are
"""

import requests
import argparse
import json
import csv

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.0"


def main():
    parser = argparse.ArgumentParser(description="VIVO Pipeline")
    parser.add_argument('--input', dest="input_filename", help="input TSV file to be loaded to VIVO", type=str)
    parser.add_argument('--output', dest="output_filename", help="output TTL file ready for loading to VIVO", type=str)
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    args = parser.parse_args()
    print(args)

    with open(args.input_filename) as tsv_file:
        reader = csv.DictReader(tsv_file, dialect='excel-tab')
        for row in reader:
            print(row)
    return


if __name__ == "__main__":
    main()
