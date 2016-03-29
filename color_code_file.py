
import argparse
import os
import sys

import re

import fileinput
from collections import namedtuple
from colorama import init
from colorama import Fore, Back, Style


Fields = namedtuple('Fields', ['date', 'time', 'pid', 'loglevel', 'modulename', 'request', 'message']) # finish adding rest of fields. Check this, not sure

LINE_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d\d:\d\d:\d\d\.\d\d\d) (?P<pid>\d+) (?P<loglevel>[A-Z]+) (?P<modulename>[^\s]+) (?P<request>([\[\w+\]-]+)?) (?P<message>.*)")

# \S for non-whitespaces
 

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
    # return_dict = {}
    lines = read_file(myfile)
    result = process_lines(lines)
    # return_dict['myfile'] = result
    return result



def process_all_files(allfiles):
    # print "allfiles: ", allfiles
    result = {}
    for f in allfiles:
        result[f] = process_file(f)
    return result




# for each line, calls the get_all_tokens() and extracts the tokens. 
# takes list of lines as input
def process_lines(lines):
    result = ""
    for line in lines:
        if (get_all_tokens(line) is None):
            result = result + line + "\n"
        else:
            result = result + color_line(get_all_tokens(line)) + "\n"
    return result




def get_all_tokens(line):
    result = LINE_RE.search(line)
    if result:
        date = result.group('date')
        time = result.group('time')
        pid = result.group('pid')
        loglevel = result.group('loglevel')
        modulename = result.group('modulename')
        request = result.group('request')
        message = result.group('message')

        # message = result.group('message')

        tokens = Fields(date, time, pid, loglevel, modulename, request, message)
        # tokens = Fields(datetime)
        # tokens = ''
    else:
        # print "tokenizing failed"
        return None
        # sys.exit(1)
    # print "tokens in get_all_tokens", tokens
    return tokens






# datetime, pid, loglevel, module name, request, message

# non greedy way of getting the request because of [] brackets thing




# maybe takes the tokens from the get_all_tokens() function and colors them. Using one of the color libaries. 
# for this maybe have to make the named tuple global
def color_line(tokens_namedtuple):
    colored_tokens = ""
    colored_tokens = colored_tokens + (Fore.RED + tokens_namedtuple.date) + " "
    colored_tokens = colored_tokens + (Fore.GREEN + tokens_namedtuple.time) + " "
    colored_tokens = colored_tokens + (Fore.YELLOW + tokens_namedtuple.pid) + " "
    colored_tokens = colored_tokens + (Fore.BLUE + tokens_namedtuple.loglevel)+ " "
    colored_tokens = colored_tokens + (Fore.MAGENTA + tokens_namedtuple.modulename) + " "
    colored_tokens = colored_tokens + (Fore.CYAN + tokens_namedtuple.request) + " " + Style.RESET_ALL
    colored_tokens = colored_tokens + tokens_namedtuple.message

    return colored_tokens


def parse_inputs():

    parser = argparse.ArgumentParser(description="color_code_file.py")

    parser.add_argument("-p", "--path", dest="PATH", help="Enter the full path to the location of the files that need to be queried' dir", required=False)
    # parser.add_argument("-d", "--date", dest="DATE", help="Enter a search date in the format YYYY-MM-DD. Ex: 2016-09-23", required=True, default="")
    # parser.add_argument("-t", "--time", dest="TIME", help="Enter a search time (24hr time) in the format hh-mm-ss.ffff. Ex: 16:23:43.231", default=None)
    # parser.add_argument("-s", "--string", dest="STRING", help="Enter a search string", default=None)
    # parser.add_argument("-v", "--verbose", action="store_true", dest="VERBOSE", help="Verbose mode", default=False)
    parser.add_argument("-f", "--files", dest="FILES", help="Enter the all the files that you want to be colored. Comma seperated, no spaces.", required=False)

    args = parser.parse_args()
    print args
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
    # test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [fasdf] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
    # test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [joain[-]wion] Guru mediation now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."

    # tuplefields = get_all_tokens(test_line1)
    # print color_line(tuplefields)
    files = []
    if args.PATH:
        files = get_all_input_files(args.PATH)
        # print "files: ", files
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
    
    args = parse_inputs()
   
    main()

#     # print "return code", rc
#     # sys.exit(rc)


