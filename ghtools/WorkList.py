import collections
import json
import logging
import os
import stat
import sys

STATUS_FILENAME = 'gt-status.json'

def status_file_exists():
    return os.path.isfile(STATUS_FILENAME)

def has_stdin():
    mode = os.fstat(0).st_mode
    return stat.S_ISFIFO(mode) or stat.S_ISREG(mode)

class WorkList:
    def __init__(self, worklistfile=None):
        self.items = []
        if worklistfile is not None:
            self.items += json.load(worklistfile, object_hook=as_WorkItem)
        elif has_stdin():
            self.items += json.load(sys.stdin, object_hook=as_WorkItem)
        elif status_file_exists(): 
            logging.info('Found gh-tools worklist file, restoring state...')
            self.item.append(json.load(file(STATUS_FILENAME)), 
                object_hook=as_WorkItem) 

    def append(self, id, item):
        if type(item) is list:
            for i in item:
                self._add_as_workitem(WorkItem(id, item))
        else:
            self._add_as_workitem(WorkItem(id, item))

    def _add_as_workitem(self, item):
        self.items = [work_item for work_item in self.items if 
            work_item.id != item.id]
        self.items.append(item)
                 
    def write(self, out):
        output = json.dumps(self.items, cls=WorkItemJSONEncoder, 
            sort_keys=True, indent=4)
        out.write(output)
        out.flush()

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        l = []
        for item in self.items:
            if item.is_status_ok():
                l.append(item)
            else:
                log('Skipping id ' + str(item.id()))
        return iter(l)

def to_unicode(v):
    if isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf8')
    else:
        return v

class WorkItemJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def as_WorkItem(dct):
    if 'id' in dct and 'status' in dct and 'data' in dct:
        return WorkItem(dct['id'], dct['data'], dct['status'])
    else:
        return dct

# Wrapper around data dict with a unique ID and some bookkeeping logic added.
class WorkItem(collections.MutableMapping):
    def __init__(self, id, wrappeddict, status='OK'):
        self.id = id
        self.status = status
        self.data = {to_unicode(k): to_unicode(v) for 
            k, v in wrappeddict.items()}

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, key):
        return self.data[to_unicode(key)]

    def __setitem__(self, key, value):
        self.data[to_unicode(key)] = to_unicode(value)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return str(self.data)

    def is_status_ok(self):
        return self.status == 'OK'

    def set_status_failed(self):
        self.status = 'FAILED'
