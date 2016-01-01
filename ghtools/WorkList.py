import collections
import json
import os
import select
import sys

STATUS_FILENAME = 'gt-status.json'

def status_file_exists():
    return os.path.isfile(STATUS_FILENAME)

def has_stdin():
    return not sys.stdin.isatty()
    # mode = os.fstat(0).st_mode
    # return stat.S_ISFIFO(mode) or stat.S_ISREG(mode)

class WorkList:
    def __init__(self, worklistfile=None):
        self.items = []
        self._worklistfile = None
        if worklistfile is not None:
            self.items += json.load(worklistfile, object_hook=self.as_WorkItem)
            self._worklistfile = worklistfile
        elif has_stdin():
            if type(sys.stdin).__name__ == 'file':
                if select.select([sys.stdin], [], [], 0)[0]:
                    self.items += json.load(sys.stdin,
                                            object_hook=self.as_WorkItem)
            else:
                input = sys.stdin.read()
                self.items += json.loads(input, object_hook=self.as_WorkItem)
        elif status_file_exists():
            self.item.append(json.load(file(STATUS_FILENAME)),
                             object_hook=self.as_WorkItem)
            self._worklistfile = open(STATUS_FILENAME, 'w')

    def append(self, data_dict):
        result = WorkItem(data_dict, self)
        self.items.append(result)
        return result

    def write(self, out):
        output = json.dumps(self.items, cls=WorkItemJSONEncoder,
                            sort_keys=True, indent=4)
        out.seek(0)
        out.write(output + '\n')
        out.flush()

    def save(self):
        with open(STATUS_FILENAME, 'w') as outfile:
            self.write(outfile)

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def as_WorkItem(self, dct):
        if 'status' in dct and 'data' in dct:
            return WorkItem(dct['data'], self, dct['status'])
        else:
            return dct

    def persist(self):
        if self._worklistfile is not None:
            self.write(self._worklistfile)

def to_unicode(v):
    if isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf8')
    else:
        return v

class WorkItemJSONEncoder(json.JSONEncoder):
    def default(self, o):
        result = o.__dict__.copy()
        del result['_work_list']
        return result

# Wrapper around data dict with some bookkeeping logic added.
class WorkItem(collections.MutableMapping):
    def __init__(self, data, work_list, status='OK'):
        self.data = {to_unicode(k): to_unicode(v) for k, v in data.items()}
        self.status = status
        self._work_list = work_list

    def __delitem__(self, key):
        del self.data[key]
        self._work_list.persist()

    def __getitem__(self, key):
        return self.data[to_unicode(key)]

    def __setitem__(self, key, value):
        self.data[to_unicode(key)] = to_unicode(value)
        self._work_list.persist()

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return str(self.data)

    def set_status_ok(self):
        self.status = 'OK'
        self._work_list.persist()

    def is_status_ok(self):
        return self.status == 'OK'

    def set_status_failed(self):
        self.status = 'FAILED'
        self._work_list.persist()

    def hello(self):
        print 'hello'