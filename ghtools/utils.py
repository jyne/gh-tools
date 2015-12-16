import datetime
import re
import sys

import pkg_resources


def log(message, out=sys.stdout):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out.write('[' + current_time + '] ' + message)
    out.flush()

def get_all_gh_languages():
    result = []
    language_list = pkg_resources.resource_string('ghtools', 'languages.yml')
    for line in language_list.splitlines():
        if line.strip().startswith('#'):
            continue 
        m = re.match('^(\S.*):', line)
        if m:
            lang = m.group(1)
            lang = lang.lower().replace('_', '__').replace(' ', '_')
            result.append(lang)
    return result
