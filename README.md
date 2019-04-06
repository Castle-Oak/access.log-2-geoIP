# access.log-2-geoIP

## Note: As of July 2018 this script requires an API access key from http://ipstack.com. Supply your API key as a command line argument. 

A quick and dirty multi-threaded script to pull location data out of your Apache logs.

Usage: `python3 get-stats.py /var/log/apache2/access.log IPStack_API_key`

Results will be dumped to the current working directory in CSV format.
