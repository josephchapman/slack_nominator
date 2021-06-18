#!/usr/bin/env python3

import sys
import argparse

from classes.bot import *

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flush', action='store_true', help='flush the cache')
    parser.add_argument('-u', '--update', action='store_true', help='update the cache')
    parser.add_argument('-s', '--select', action='store_true', help='select someone')
    args = parser.parse_args()


    bot = Bot()


    if args.flush:
        print('Option selected: Flush')
        bot.cache.flush()
    if args.update:
        print('Option selected: Update')
        bot.cache.update()
    if args.select:
        print('Option selected: Select')
        bot.select()
    if len(sys.argv) == 1:
        print('No option selected: Defaulting to Assign')
        bot.assign()



if __name__ == '__main__':
    main()
