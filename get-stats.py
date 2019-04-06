#!/usr/bin/env python3
import urllib3
import json
import numpy
import sys
import socket
import time
from multiprocessing.dummy import Pool


def apiGet(ip):
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


def main():
    IPUnsort = []
    for line in open(logPath, 'r'):
        Entry = line.split()
        IPUnsort.append(Entry[0])

    IPUnique = numpy.unique(IPUnsort)

    threadCount = len(IPUnique)

    print("Querying entries in", logPath, "with", str(threadCount), "threads.\n")

    with Pool(threadCount) as thread:
        thread.map(apiGet, IPUnique)

    thread.close()
    thread.join()

    coreSorted = sorted(coreRaw)
    coreFinal = '\n'.join(coreSorted)

    with open(outputPath, 'a+') as template:
        template.write(coreFinal)

    print("\n", logPath, " - Successful!\n")
    print("Results have been saved to", outputPath, "\n")


if __name__ == "__main__":
    try:
        logPath = sys.argv[1]
        userKey = sys.argv[2]
    except:
        print("\nLog path cannot be empty.\n")
        print("Usage: ./get-stats.py /var/log/apache2/access.log IPStack_API_Key\n")
        print("Results will be dumped to the current working directory in CSV format.\n")
        quit()

    try:
        open(logPath, 'r')
    except:
        print("\nError reading log file\n")
        print("Verify file path and permissions.\n")
        quit()

    # Some variables for easy access.
    outputPath = str(time.time()) + "-output.csv"
    apiDomain = 'http://api.ipstack.com/'
    apiKey = '?access_key={}'.format(userKey)

    coreRaw = []
    main()
