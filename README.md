# access.log-2-geoIP

## Note: As of July 2018 this script requires an API access key from http://ipstack.com. Registration is free. Paste your key into the apiKey string.

A quick and dirty multi-threaded script to pull location data out of your Apache logs.

Usage: ./get-stats.py /var/log/apache2/access.log

Results will be dumped to the current working directory in CSV format.
