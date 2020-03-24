#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-grant: from a source (the command line),
    return a grant metadata object

    kind         'grant'
    identifier   string
    grantor      string
    country      string




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


def main():
    parser = argparse.ArgumentParser(description="extract grant for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--identifier", dest="identifier", required=True,
                        help="a grant identifier.  Identifiers vary by grantor", metavar="identifier",
                        type=str)
    parser.add_argument("--grantor", dest="grantor", required=True,
                        help="name of agency making the grant.", metavar="grantor",
                        type=str)
    parser.add_argument("--country", dest="country", required=True,
                        help="country in which award was made", metavar="country",
                        type=str)
    parser.add_argument("--date", dest="date", required=True,
                        help="date of award", metavar="date",
                        type=str)
    args = parser.parse_args()

    if args.verbose > 0:
        print(args)
    grant = perfect_grant(args.identifier, args.grantor, args.country, args.date)
    print(grant)
    return


if __name__ == "__main__":
    main()
