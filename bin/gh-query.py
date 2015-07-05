#!/usr/bin/env python
import argparse
import os
import re
import requests
import signal
import string
import sys
import urllib

def signal_handler(signal, frame):
    os._exit(0)
signal.signal(signal.SIGINT, signal_handler)

def do_rest_call(rest_service, parameters={}):
	return do_url_call('https://api.github.com' + rest_service, parameters)

def get_gh_token():
    secret_file = os.path.join(os.path.expanduser("~"), ".github-secret")
    if not os.path.isfile(secret_file):
        print "Could not find .github-secret file in home directory!"
        os._exit(1)
    with open(secret_file, 'r') as f:
        return f.readline().strip()

def do_url_call(url, parameters={}):
    result = requests.get(url, params=parameters,
        auth=(get_gh_token(), 'x-oauth-basic'))
    return result

def get_language_info(repo):
	response = do_url_call(repo['languages_url'])
	return response.json()

def get_projects_data(response):
    result = []
    items = response.json()['items']
    for repo in items:
        project_data = string.join([str(repo['id']), repo['html_url'], 
            repo['name'], str(repo['language']), repo['created_at']], ',') 
        result.append(project_data)
    return result

def has_next_page(response):
    pagination_links = response.headers['link']
    if pagination_links is None:
        return False
    m = re.search('[<]([^>]+)[>]; rel="next"', pagination_links)
    return m is not None

def get_next_page_url(response):
    pagination_links = response.headers['link']
    m = re.search('[<]([^>]+)[>]; rel="next"', pagination_links)
    return m.group(1)

def get_last_page_number(response):
    pagination_links = response.headers['link']
    if pagination_links is None:
        return 1
    m = re.search('[<].*[?&]page=(\d+).*[>]; rel="last"', pagination_links)
    return m.group(1)

def show_results(projects, args):
    report = 'id,url,name,language,created_at\n'
    for p in projects:
        report += p + '\n'
    if args.outfile is not None:
        args.outfile.write(report)
        args.outfile.close()
        print "Written to file: " + str(args.outfile.name)
    else:
        print report

def do_query(query_opts):
    response = do_rest_call('/search/repositories', query_opts)
    print "Pages in search result: " + str(get_last_page_number(response))
    sys.stdout.write("Please wait while retrieving page: ")
    result = get_projects_data(response)
    page = 1
    sys.stdout.write(str(page))
    sys.stdout.flush()
    while has_next_page(response):
        page += 1
        response = do_url_call(get_next_page_url(response))
        result.extend(get_projects_data(response))
        sys.stdout.write(' ' + str(page))
        sys.stdout.flush()
    print
    print "Total repositories: " + str(len(result))
    return result
    
parser = argparse.ArgumentParser(description="Query GitHub search API")
parser.add_argument('-q', '--query', default='') 
parser.add_argument('-l', '--language', action='append')
parser.add_argument('-o', '--outfile', type=argparse.FileType('w', 0),
    help="Write CSV output to this file") 
args = parser.parse_args()

if args.query == '' and args.language is None:
    parser.print_help()
    sys.exit()

args.query += ' in:name,description'
query_opts = {'q': args.query, 'per_page': '100'}
projects = []
if args.language is None:
    projects.extend(do_query(query_opts))
else:
    for l in args.language: 
        print "Querying GitHub for language: " + l
        query_opts['q'] = (args.query + ' language:' + l)
        projects.extend(do_query(query_opts))
show_results(projects, args)
