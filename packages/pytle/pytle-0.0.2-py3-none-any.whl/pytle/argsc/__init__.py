# from __future__ import print_function
import argparse
import logging
#from .observer import observer
#import ephem
# import grid
# from datetime import datetime
#import pytz

class argsc:
    """ A class to generate command-line args and properties """

    def __init__(self, arguments):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument('-k', '--keps-url', help="Keplerian Elements URL", default='http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt')
        parser.add_argument('-s', '--sats', help="Satellites to track", default='SO-50,AO-85')
        #parser.add_argument('-g', '--generate-days', help="Days to generate events +/- today", default=30)
        #parser.add_argument('-d', '--generate-degrees', help="Only show passes greater than x degrees", default=5)
        #parser.add_argument('-a', '--alert-min', help="Alert x min ahead of events", default=15)

        #parser.add_argument('-y', '--ymd', help="Only show passes for day YYYYMMDD", default=None)

        #parser.add_argument('-l', '--lat-long', help="Latitude and Longitude of observer", default=None)
        #parser.add_argument('-m', '--grid', help="Grid square of observer", default=None)

        parser.add_argument('-o', '--output', help="Output Format (text, json)", default='text')

        parser.add_argument('-i', '--info', dest='info', action='store_true', help="Print info debugging messages", default=False)
        parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="Print verbose debugging messages", default=False)
        parser.add_argument('-t', '--trace', dest='trace', action='store_true', help="Print more verbose debugging messages", default=False)
        args = parser.parse_args(arguments)

        # Set log levels
        args.log_level = logging.WARN
        if args.info:
            args.log_level = logging.INFO

        if args.verbose or args.trace:
            args.log_level = logging.DEBUG

        # Make sats an array
        if args.sats:
            if ',' in args.sats:
                args.sats = args.sats.split(',')
            else:
                args.sats = [args.sats]

#        # Check for a grid square
#        if not args.grid:
#            raise AssertionError("Please give a grid")
#
#        if isinstance(args.generate_degrees, str):
#            args.generate_degrees = int(args.generate_degrees)
#
#        if isinstance(args.alert_min, str):
#            args.alert_min = int(args.alert_min)
#
#        if isinstance(args.generate_days, str):
#            args.generate_days = int(args.generate_days)
#
#        ob = observer(args)
#        args.obs = ob.obs
#
#        if args.ymd:
#            args.start_date = ephem.Date(datetime(int(args.ymd[0:4]), int(args.ymd[4:6]), int(args.ymd[6:8]), tzinfo=pytz.utc))
#            args.end_date = args.start_date + (24 * ephem.hour)
#
#        if args.generate_days and not args.ymd:
#            args.start_date = ephem.Date(args.obs.date - (int(args.generate_days) * 24 * ephem.hour))
#            args.end_date = ephem.Date(args.obs.date + (int(args.generate_days) * 24 * ephem.hour))
#
#        # # Figure out observer location
#        # if args.lat_long and not args.grid:
#        #     args.lat_long = [float(l) for l in args.lat_long.split(",")]
#        #     args.grid = grid.toMaiden(args.lat_long, precision=3)
#
#        # if args.grid and not args.lat_long:
#        #     args.lat_long = grid.toLoc(args.grid)
#
        self.args = args
#
#    def get_args(self):
#        return self.args

# if __name__ == "__main__":
#     import sys
#     args = argsc.get_args(sys.argv[1:])
#     print(args)
