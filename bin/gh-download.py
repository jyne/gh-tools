#!/usr/bin/env python
import csv
import datetime
import mysql.connector
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib
import zipfile

homedir = os.path.expanduser("~")
os.environ["PATH"] += os.pathsep + os.path.join(homedir, 'bin')

def signal_handler(signal, frame):
    os._exit(0)
signal.signal(signal.SIGINT, signal_handler)

def log(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '[' + current_time + '] ' + message
    sys.stdout.flush()

def get_systems(filename):
    result = []
    file = open(filename, 'rU')
    contents = csv.reader(file)
    next(contents)
    for row in contents:
        id = row[0]
        url = row[1]
        name = row[2]
        language = row[3]
        result.append({'id': id, 'name': name, 'url': url, 
            'language': language}) 
    return result

def download_and_extract_codebase(system, directory):
    log("Downloading sources for: " + system['name'] + "...")
    zippedArchiveFile = tempfile.NamedTemporaryFile()
    urllib.urlretrieve(system['url'] + '/archive/master.zip', 
        zippedArchiveFile.name)
    zipf = zipfile.ZipFile(zippedArchiveFile.name, 'r')
    zipf.extractall(directory)
    zippedArchiveFile.close()

def get_project_ids_from_csv_file(filename):
    result = set()
    lines = open(filename, 'r').readlines() 
    if len(lines) > 0:
        del lines[0] # Skip header
    for line in lines:
        m = re.match('^"(\\d+)",.*', line)
        if m is not None:
            result.add(long(m.group(1)))
    return result

if (len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]) 
        or not os.path.isdir(sys.argv[2])):
    usage = """
usage: $SCRIPTNAME <CSV file> <destionation directory>

The CSV input file should have a header row and the following row format:
project-id,github-repo-url,project-name,project-language,created-at

For example:
169166,https:/github.com/c1982/togi,togi,C#,2009-04-06T09:18:52Z
"""
    print usage.replace('$SCRIPTNAME', sys.argv[0])
    sys.exit()

already_analyzed = set()
if os.path.isfile('failed-projects.csv'):
    log("Found existing failed projects file (failed-projects.csv)")
    already_analyzed |= get_project_ids_from_csv_file('failed-projects.csv')
    failedfile = open('failed-projects.csv', 'a+')
else:
    failedfile = open('failed-projects.csv', 'w')
    failedfile.write('"Project ID","Project name"\n')
    failedfile.flush()

if os.path.isfile('gh-projects-data.csv'):
    log("Found existing project data file (gh-projects-data.csv)")
    already_analyzed |= get_project_ids_from_csv_file('gh-projects-data.csv')
    outfile = open('gh-projects-data.csv', 'a+')
    outcsv = csv.writer(outfile, quotechar='"', quoting=csv.QUOTE_ALL)
else:
    outfile = open('gh-projects-data.csv', 'w')
    outcsv = csv.writer(outfile, quotechar='"', quoting=csv.QUOTE_ALL)
    outcsv.writerow(['Project ID', 'URL', 'Project name', 'Language'])
    outfile.flush()

for system in get_systems(sys.argv[1]):
    destdir = os.path.join(sys.argv[2], system['name'])
    try:
        id = long(system['id'])
        if (id in already_analyzed):
            log("Skipping project: " + str(id) + " (already analyzed)")
            continue
        download_and_extract_codebase(system, destdir)
    except:
        print "Error in downloading codebase: " + system['name']
        print sys.exc_info()
        print "On line: " + format(sys.exc_info()[-1].tb_lineno)
        failedfile.write('"' + system['id'] + '","' + system['name'] + '"\n')
        failedfile.flush()
