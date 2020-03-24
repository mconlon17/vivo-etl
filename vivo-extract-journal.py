#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-journal: from a source (the command line),
    return a journal metadata object

    kind         'journal'
    issn    string
    title     string
    iso-abbreviation      string




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


def perfect_journal(issn, title, isoabbrev):
    from datetime import datetime

    m = dict(kind='journal')
    m['extract_date'] = perfect_date(datetime.today().strftime('%Y%m%d'))

    m['issn'] = issn
    m['title'] = title
    m['iso-abbreviation'] = isoabbrev

    return m


def main():
    parser = argparse.ArgumentParser(description="extract journal for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--issn", dest="issn", required=True,
                        help="the issn of the journal.", metavar="issn",
                        type=str)
    parser.add_argument("--title", dest="title", required=True,
                        help="the full journal title", metavar="title",
                        type=str)
    parser.add_argument("--isoabbrev", dest="isoabbrev", required=True,
                        help="The ISO Abbreviated title", metavar="isoabbrev",
                        type=str)
    args = parser.parse_args()

    if args.verbose > 0:
        print(args)
    journal = perfect_journal(args.issn, args.title, args.isoabbrev)
    print(journal)
    return


if __name__ == "__main__":
    main()
