#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from pytle.pytle import main
from pytle import pytle
from pytle.argsc import argsc


def main():
    import sys
    args = argsc(sys.argv[1:])
    tle = pytle(keps_url="http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt", cache=True)
    for sat in args.args.sats:
        if args.args.output == "text":
            print(tle.get_sat_info_text(sat))
        elif args.args.output == "json":
            print(tle.get_sat_info_json(sat))


if __name__ == '__main__':
    main()
