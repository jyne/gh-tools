import json
import os
import StringIO
import sys
import tempfile 
from unittest import TestCase

from ghtools import WorkList

class test_WorkList(TestCase):
    
    def test_status_file_exists_no_status_file(self):
        WorkList.STATUS_FILENAME = '/file/does/not/exists'

        self.assertFalse(WorkList.status_file_exists())

    def test_status_file_exists_has_status_file(self):
        tmpfile = tempfile.mkstemp()[1] 
        WorkList.STATUS_FILENAME = os.path.abspath(tmpfile)

        self.assertTrue(WorkList.status_file_exists())

    def test_WorkItem_wraps_around_dict(self):
        d = {'id': 123, 'a': 1, 'b': 2}
        wi = WorkList.WorkItem(d)

        self.assertEquals(123, wi['id'])
        self.assertEquals(1, wi['a'])

        del wi['a']

        self.assertFalse('a' in wi)

    def test_WorkItem_set_status(self):
        wi = WorkList.WorkItem({})

        self.assertTrue(wi.is_status_ok())

        wi.set_status_failed()
        
        self.assertFalse(wi.is_status_ok())

    def test_empty_WorkList(self):
        wl = WorkList.WorkList()
        
        self.assertEquals(0, len(wl.items))

        d = {'id': 123, 'a': 1234}
        wl.append(d)

        self.assertEquals(1, len(wl.items))

        for wi in wl:
            self.assertEquals(1234, wi['a'])

    def test_write_WorkList(self):
        wl = WorkList.WorkList()
        wl.append({'id': 123, 'a': 1234})
        wl.append({'id': 456, 'b': 5678})
        out = StringIO.StringIO()

        wl.write(out)  
        result = json.loads(out.getvalue())

        self.assertEquals(2, len(result))
        self.assertEquals(123, result[0]['data']['id'])
        self.assertEquals(456, result[1]['data']['id'])

        out.close()

    def test_load_WorkList_from_inputstream(self):
        s = '[{"status": "FAILED", "data": {"id": 123, "a": 1}}, '
        s += '{"status": "OK", "data": {"id": 456, "b": 2}}]'
        inputstream = StringIO.StringIO(s)
        
        wl = WorkList.WorkList(inputstream)

        self.assertEquals(2, len(wl))
        self.assertEquals(123, wl[0]['id'])
        self.assertEquals(456, wl[1]['id'])

    def test_load_WorkList_from_stdin(self):
        stdin = sys.stdin
        has_stdin = WorkList.has_stdin

        s = '[{"status": "FAILED", "data": {"id": 789, "a": 1}}, '
        s += '{"status": "OK", "data": {"id": 246, "b": 2}}]'
        sys.stdin = StringIO.StringIO()
        sys.stdin.write(s)
        sys.stdin.seek(0)
        WorkList.has_stdin = lambda: True
        
        wl = WorkList.WorkList()

        self.assertEquals(2, len(wl))
        self.assertEquals(789, wl[0]['id'])
        self.assertEquals(246, wl[1]['id'])

        sys.stdin = stdin
        WorkList.has_stdin = has_stdin
