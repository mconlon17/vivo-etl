#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-person: from a source (the command line),
    return a person metadata object

    kind         'person'
    extract_date date metadata data
    orcid   string
    local_id
    name      string
    first_name string
    last_name string
    affiliation string





"""

import argparse

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.0.1"


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


def perfect_person(orcid):
    from datetime import datetime

    m = dict(kind='person')
    m['extract_date'] = perfect_date(datetime.today().strftime('%Y%m%d'))

    # make a call to the orcid public api and parse the results

    m['orcid'] = orcid
    m['local_id'] = ''
    m['name'] = ''
    m['first_name'] = ''
    m['last_name'] = ''
    m['affiliation string'] = ''
    return m


def main():
    parser = argparse.ArgumentParser(description="extract person for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--orcid", dest="orcid", required=True,
                        help="ORCiD for the person", metavar="orcid",
                        type=str)
    args = parser.parse_args()

    if args.verbose > 0:
        print(args)
    person = perfect_person(args.orcid)
    print(person)
    return


if __name__ == "__main__":
    main()
