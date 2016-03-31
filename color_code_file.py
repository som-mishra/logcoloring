#!/usr/bin/env python

import argparse
import fileinput
import os
import re
import sys

from colorama import init
from collections import namedtuple
from colorama import Fore, Back, Style


Fields = namedtuple('Fields', ['date', 'time', 'pid', 'loglevel', 'modulename', 'request', 'message'])

LINE_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d\d:\d\d:\d\d\.\d\d\d) (?P<pid>\d+) (?P<loglevel>[A-Z]+) (?P<modulename>[^\s]+) (?P<request>([\[\w+\]-]+)?) (?P<message>.*)")
LINE_RE_NOPID = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d\d:\d\d:\d\d\.\d\d\d) (?P<loglevel>[A-Z]+) (?P<modulename>[^\s]+) (?P<request>([\[\w+\]-]+)?) (?P<message>.*)")


def read_file(inputfile):
    lines = []
    with open(inputfile) as f:
        for line in f:
            lines.append(line.rstrip())
    return lines


def get_all_input_files(mypath):
    files = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f.endswith(('.txt', '.txt.gz')))]
    return files


def process_file(myfile):
    lines = read_file(myfile)
    result = process_lines(lines)
    return result


def process_all_files(allfiles):
    result = {}
    for f in allfiles:
        result[f] = process_file(f)
    return result


def process_lines(lines):
    result = ""
    for line in lines:
        if (get_all_tokens(line) is None):
            result = result + line + "\n"
        else:
            result = result + color_line(get_all_tokens(line)) + "\n"
    return result


def get_all_tokens(line):
    pid = ""
    result = LINE_RE.search(line)
    if result:
        date = result.group('date')
        time = result.group('time')
        pid = result.group('pid')
        loglevel = result.group('loglevel')
        modulename = result.group('modulename')
        request = result.group('request')
        message = result.group('message')
    else:
        result = LINE_RE_NOPID.search(line)
        if result:
            date = result.group('date')
            time = result.group('time')
            loglevel = result.group('loglevel')
            modulename = result.group('modulename')
            request = result.group('request')
            message = result.group('message')
        else:
            return None

    tokens = Fields(date, time, pid, loglevel, modulename, request, message)
    return tokens


def color_line(tokens_namedtuple):
    colored_tokens = ""
    colored_tokens = colored_tokens + (Fore.RED + tokens_namedtuple.date) + " "
    colored_tokens = colored_tokens + (Fore.GREEN + tokens_namedtuple.time) + " "
    colored_tokens = colored_tokens + (Fore.YELLOW + tokens_namedtuple.pid) + " "
    colored_tokens = colored_tokens + (Fore.BLUE + tokens_namedtuple.loglevel) + " "
    colored_tokens = colored_tokens + (Fore.MAGENTA + tokens_namedtuple.modulename) + " "
    colored_tokens = colored_tokens + (Fore.CYAN + tokens_namedtuple.request) + " " + Style.RESET_ALL
    colored_tokens = colored_tokens + tokens_namedtuple.message

    return colored_tokens


def parse_inputs():

    parser = argparse.ArgumentParser(description="color_code_file.py")

    parser.add_argument("-p", "--path", dest="PATH", help="Enter the full path to the location of the files that need to be colored. For ex $ ./color_code_file.py -p /home/smishra/colorlog/", required=False)
    parser.add_argument("-f", "--files", dest="FILES", help="Enter one or that you want to be colored. Comma seperated, no spaces. For ex: $ ./color_code_file.py -f log.txt log2.txt ", required=False)
    parser.add_argument("-v", "--verbose", action="store_true", dest="VERBOSE", help="Verbose mode", default=False)

    args = parser.parse_args()
    # print args
    if (args.PATH is None and args.FILES is None and sys.stdin.isatty() is True):
        print "Must provide either a path, files, or pipe input into the program. For example: $ cat log.txt | ./color_code_file.py. Use -h for help"
        sys.exit(1)
    if (args.PATH is not None):
        if not os.path.exists(args.PATH):
            print ("Path:[%s] does not exist. Check your input." % args.PATH)
            sys.exit(1)
    elif(args.FILES is not None):
        args.FILES = args.FILES.split(',')
        for f in args.FILES:
            if not os.path.exists(f):
                print ("File:[%s] does not exist. Check your input." % f)
                sys.exit(1)
    return args


def main():
    args = parse_inputs()
    if args.VERBOSE:
        print "args:", args
    if (args.PATH is None and args.FILES is None):
        lines = []
        filelines = sys.stdin
        for line in filelines:
            lines.append(line.rstrip())
        print process_lines(lines)
    else:
        files = []
        if args.PATH:
            files = get_all_input_files(args.PATH)
        elif args.FILES:
            files = args.FILES

        result = process_all_files(files)
        for key in result:
            print "File=", key, "\n", result[key]

    print(Style.RESET_ALL)


if __name__ == '__main__':
    #Use 2.7 version of python
    ver = (2, 7)
    if sys.version_info[:2] != ver:
        print("ERROR: Use Python Version: 2.7")
        sys.exit()
    main()
