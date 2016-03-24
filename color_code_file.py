import sys

import re

import fileinput
from collections import namedtuple
from colorama import init
from colorama import Fore, Back, Style


Fields = namedtuple('Fields', ['date', 'time', 'pid', 'loglevel', 'modulename', 'request', 'message']) # finish adding rest of fields. Check this, not sure

LINE_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d\d:\d\d:\d\d\.\d\d\d) (?P<pid>\d+) (?P<loglevel>[A-Z]+) (?P<modulename>[^\s]+) (?P<request>([\[\w+\]-]+)?) (?P<message>.*)")

# def read_file ():
#     # if myinputfile.endswih('.gz'):
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
    return tokens






# datetime, pid, loglevel, module name, request, message

# non greedy way of getting the request because of [] brackets thing




# maybe takes the tokens from the get_all_tokens() function and colors them. Using one of the color libaries. 
# for this maybe have to make the named tuple global
def color_line(tokens_namedtuple):
    colored_tokens = ""
    # print(Fore.RED + tokens_namedtuple.date)
    colored_tokens = colored_tokens + (Fore.RED + tokens_namedtuple.date) + " "
    colored_tokens = colored_tokens + (Fore.GREEN + tokens_namedtuple.time) + " "
    colored_tokens = colored_tokens + (Fore.YELLOW + tokens_namedtuple.pid) + " "
    colored_tokens = colored_tokens + (Fore.BLUE + tokens_namedtuple.loglevel)+ " "
    colored_tokens = colored_tokens + (Fore.MAGENTA + tokens_namedtuple.modulename) + " "
    colored_tokens = colored_tokens + (Fore.CYAN + tokens_namedtuple.request) + " " + Style.RESET_ALL
    colored_tokens = colored_tokens + tokens_namedtuple.message

    return colored_tokens




# # for each line, calls the get_all_tokens() and extracts the tokens. 
# def process_lines(lines):
#     for line in lines:
#         result = color_lines(get_all_tokens(lines))







def main():
    # test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [fasdf] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
    test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [joain[-]wion] Guru mediation now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."

    #tuplefields = Fields(date='2016-04-07', time='23:08:02.123', pid='26887', loglevel='WARNING', modulename='guru_meditation_report', request='[joain[-]wion]')
    tuplefields = get_all_tokens(test_line1)
    print color_line(tuplefields)
    # print test_line1[tuplefields.request:]
    print(Style.RESET_ALL)
    # print get_all_tokens(test_line1)
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


