from unittest import TestCase
from StringIO import StringIO

import ghtools.utils

class utilsTest(TestCase):

    def test_log(self):
        out = StringIO()

        ghtools.utils.log("Hello world!", out=out)
        result = out.getvalue().strip()

        self.assertTrue(result.endswith("Hello world!"))
