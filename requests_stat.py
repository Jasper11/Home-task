# !user/bin/python

import datetime

current_date = 'Date'
current_count = '		      Amount'

def parse_line(line):
    strings = line.split(' ')
    #print strings[3]
    #date = datetime.datetime.strptime( "[2012-10-09T19:00:55Z", "[%Y-%m-%dT%H:%M:%SZ" )
    # [15/Oct/2014:17:49:58
    global current_date
    global current_count
    if (strings[8] == '200'):
      date = datetime.datetime.strptime(strings[3], '[%d/%b/%Y:%H:%M:%S')
      #print date
      date = date.replace(minute = 0, second = 0)
    else:
      return;
      
    if current_date == date and strings[8] == '200':
       current_count = current_count + 1
       
    else:
	if current_date == 'Date':
	   print current_date, current_count
	else:
	   current_date2 = current_date.replace(minute = 59, second = 59)
	   print current_date, '-', current_date2, current_count
	current_date = date
	current_count = 1
    return;

#parse_line();  

try:
  while True:
    parse_line(raw_input())
except EOFError:
   current_date2 = current_date.replace(minute = 59, second = 59)
   print current_date, '-', current_date2, current_count

