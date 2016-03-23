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
from collections import namedtuple
from colorama import init


# def read_file ():
#     # if myinputfile.endswith('.gz'):
#     #     with gzip.open(myinputfile, 'rb') as f:
#     #         filecontent = f.readlines()
#     # else:
#     #     with open(myinputfile, 'rb') as f:
#     #         filecontent = f.readlines()
#     lines = []
#     for line in fileinput.input():
#         line.rstrip()
#         lines.append(line)
#     return lines
# [a-z_\.]
# \[\w+\]

def get_all_tokens(line):
    #Fields = namedtuple('Fields', ['datetime', 'pid', 'loglevel', 'modulename', 'request']) # finish adding rest of fields. Check this, not sure
    Fields = namedtuple('Fields', ['date', 'time', 'pid', 'loglevel', 'modulename', 'request']) # finish adding rest of fields. Check this, not sure

    #LINE_RE = re.compile^(('?P<datetime>\d{4}-\d{2}-\d{2}')('?P<pid>\d{5}')('?P<loglevel>[A-Z]')('?P<modulename>[a-z\.]')('?P<request>\[*?\]')) # finish adding the regex's for the rest of the fields
    #LINE_RE = re.compile(r'(?P<datetime>\d{4}-\d{2}-\d{2} \d\d:\d\d:\d\d\.\d\d\d)(?P<pid>\d+)') # finish adding the regex's for the rest of the fields
    result = re.match(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d\d:\d\d:\d\d\.\d\d\d) (?P<pid>\d+) (?P<loglevel>[A-Z]+) (?P<modulename>[^\s]+) (?P<request>\[\-\])", line)
    # print "line re", LINE_RE
    # result = LINE_RE.search(line)
    if result:
        date = result.group('date')
        time = result.group('time')
        pid = result.group('pid')
        loglevel = result.group('loglevel')
        modulename = result.group('modulename')
        request = result.group('request')
        # message = result.group('message')

        tokens = Fields(date, time, pid, loglevel, modulename, request)
        # tokens = Fields(datetime)
        # tokens = ''
    return tokens






# datetime, pid, loglevel, module name, request, message

# non greedy way of getting the request because of [] brackets thing




# maybe takes the tokens from the get_all_tokens() function and colors them. Using one of the color libaries. 
# for this maybe have to make the named tuple global
# def color_line(tokens_namedtuple):
#     colored_tokens = []
#     colored_tokens.append(Fore.RED + tokens_namedtuple.datetime)
#     colored_tokens.append(Fore.GREEN + tokens_namedtuple.pid)
#     colored_tokens.append(Fore.YELLOW + tokens_namedtuple.loglevel)
#     colored_tokens.append(Fore.BLUE + tokens_namedtuple.modulename)
#     colored_tokens.append(Fore.MAGENTA + tokens_namedtuple.request)
#     colored_tokens.append(Fore.CYAN + tokens_namedtuple.message)
#     return colored_tokens




# # for each line, calls the get_all_tokens() and extracts the tokens. 
# def process_lines(lines):
#     for line in lines:
#         result = color_lines(get_all_tokens(lines))







def main():
    test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."

    print get_all_tokens(test_line1)
    # lines = read_file()

    # process_lines(lines)




if __name__ == '__main__':
    #Use 2.7 version of python
    ver = (2, 7)
    if sys.version_info[:2] != ver:
        print("ERROR: Use Python Version: 2.7")
        sys.exit()
    

    main()

#     # print "return code", rc
#     # sys.exit(rc)


