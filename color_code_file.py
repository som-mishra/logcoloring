#!/usr/bin/python

import sys
import gzip
import traceback
import getopt
from os import listdir
from os.path import isfile, join
from datetime import datetime

import argparse
import datetime
import gzip
import os
import re
import sys

import fileinput
for collections import namedtuple
for colorama import init


def read_file ():
    # if myinputfile.endswith('.gz'):
    #     with gzip.open(myinputfile, 'rb') as f:
    #         filecontent = f.readlines()
    # else:
    #     with open(myinputfile, 'rb') as f:
    #         filecontent = f.readlines()
    lines = []
    for line in fileinput.input():
        line.rstrip()
        lines.append(line)
    return lines


def get_all_tokens(line):
    Fields = namedtuple('Fields', ['datetime', 'pid', 'loglevel', 'modulename', 'request', 'message']) # finish adding rest of fields. Check this, not sure

    LINE_RE = re.compile^( ('?P<datetime>\d{4}-\d{2}-\d{2}') ('?P<pid>\d{5}') () () () () ) # finish adding the regex's for the rest of the fields
    result = LINE_RE.search(line)
    if result:
        datetime = results.group('datetime')
        pid = results.group('pid')
        loglevel = results.group('loglevel')
        modulename = results.group('modulename')
        request = results.group('request')
        message = results.group('message')

        tokens = Fields(datetime, pid, loglevel, modulename, request, message)

    return tokens


# datetime, pid, loglevel, module name, request, message

# non greedy way of getting the request because of [] brackets thing




# maybe takes the tokens from the get_all_tokens() function and colors them. Using one of the color libaries. 
def color_lines(tokens):




# for each line, calls the get_all_tokens() and extracts the tokens. 
def process_lines(lines):
    for line in lines:
        get_all_tokens(lines)

    






    





def main():
    lines = read_file()

    process_lines(lines)




if __name__ == '__main__':
    #Use 2.7 version of python
    ver = (2, 7)
    if sys.version_info[:2] != ver:
        print("ERROR: Use Python Version: 2.7")
        sys.exit()
    

        main()

    # print "return code", rc
    # sys.exit(rc)
