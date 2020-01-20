#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    vivo-extract-date: from a source (the command line),
    return a date metadata object, a dict with two keys -- date and precision

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
        m['date'] = datetime.strptime(val, '%Y')
        m['precision'] = 'year'
    elif len(val) == 6:
        m['date'] = datetime.strptime(val, '%Y%m')
        m['precision'] = 'month'
    elif len(val) == 8:
        m['date'] = datetime.strptime(val, '%Y%m%d')
        m['precision'] = 'day'
    else:
        raise argparse.ArgumentError(val + ' an unknown date')
    return m


def main():
    parser = argparse.ArgumentParser(description="extract date for VIVO")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--date", dest="date", required=True,
                        help="a date value", metavar="DATE",
                        type=perfect_date)
    args = parser.parse_args()
    if args.verbose > 0:
        print(args.date)
    if args.verbose > 1:
        print(args.date['date'])
    print(args.date)
    return


if __name__ == "__main__":
    main()
