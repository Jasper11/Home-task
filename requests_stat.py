# !user/bin/python

import datetime

def parse_line(line):
    strings = line.split(' ')
    print strings[3]
    #date = datetime.datetime.strptime( "[2012-10-09T19:00:55Z", "[%Y-%m-%dT%H:%M:%SZ" )
    date = datetime.datetime.strptime(strings[3], '[%d/%b/%Y:%H:%M:%S')
    print date
    date = date.replace(minute = 0, second = 0)
    # [15/Oct/2014:17:49:58
    print date
    return;

#parse_line();  

while True:
    parse_line(raw_input())