#!/usr/bin/env python3
import urllib3
import json
import numpy
import os
import sys
import socket
import time
import re
from multiprocessing.dummy import Pool

# Check validity of log path.
try:
    logPath = sys.argv[1]
except:
    print("\nLog path cannot be empty.\n")
    print("Usage: ./get-stats.py /var/log/apache2/access.log\n")
    print("Results will be dumped to the current working directory in CSV format.\n")
    quit()

try:
    open(logPath, 'r')
except:
    print("\nError reading log file\n")
    print("Verify file path and permissions.\n")
    quit()

# Some variables for easy access.
outputPath = str(time.time()) + "-output.txt"
apiDomain = 'freegeoip.net/json/' # This script will be rewritten for IPStack after July 1st 2018.
threadCount = 64 # This is the number of concurrent connections to the API.

print("Querying entries in", logPath, "with", str(threadCount), "threads.\n")

coreRaw = []
def main(ip):
    global coreList
    call = apiDomain + ip
    http = urllib3.PoolManager()
    query = http.request('GET', call)
    response = json.loads(query.data.decode('utf-8'))
    city = response['city']
    if city == "":
        city = "None"
    state = response['region_name']
    if state == "":
        state = "None"
    try:
        ptr = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        ptr = "NO PTR"
    output = ip + "," + ptr + "," + city + "," + state
    coreRaw.append(output)

IPUnsort = []
for line in open(logPath, 'r'):
    Entry = line.split()
    IPUnsort.append(Entry[0])

IPUnique = numpy.unique(IPUnsort)

with Pool(threadCount) as thread:
    thread.map(main, IPUnique)

thread.close()
thread.join()

coreSorted = sorted(coreRaw)
coreFinal = '\n'.join(coreSorted)

with open(outputPath, 'a+') as template:
    template.write(coreFinal)

print(logPath, " - Successful!\n")
print("Results have been saved to", outputPath, "\n")
