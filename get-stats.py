#!/usr/bin/env python3
import urllib3
import json
import numpy
import os
import sys
import socket
import time
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
apiDomain = 'http://api.ipstack.com/' # This script will be rewritten for IPStack after July 1st 2018.
apiKey = '?access_key=#Paste_API_Key_Here'

print("Querying entries in", logPath, "with", str(threadCount), "threads.\n")

coreRaw = []
def main(ip):
    call = apiDomain + ip + apiKey
    http = urllib3.PoolManager()
    query = http.request('GET', call)
    response = json.loads(query.data.decode('utf-8'))
    city = response['city']
    if city is None:
        city = "None"
    region = response['region_name']
    if region is None:
        region = response['country_name']
        if region is None:
            region = "None"
    try:
        ptr = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        ptr = "NO PTR"
    output = ip + "," + ptr + "," + city + "," + region
    coreRaw.append(output)
    print(output)

IPUnsort = []
for line in open(logPath, 'r'):
    Entry = line.split()
    IPUnsort.append(Entry[0])

IPUnique = numpy.unique(IPUnsort)

threadCount = len(IPUnique)

with Pool(threadCount) as thread:
    thread.map(main, IPUnique)

thread.close()
thread.join()

coreSorted = sorted(coreRaw)
coreFinal = '\n'.join(coreSorted)

with open(outputPath, 'a+') as template:
    template.write(coreFinal)

print("\n", logPath, " - Successful!\n")
print("Results have been saved to", outputPath, "\n")
