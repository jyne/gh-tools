from unittest import TestCase
from StringIO import StringIO

import ghtools.utils

class utilsTest(TestCase):

    def test_log(self):
        out = StringIO()

        ghtools.utils.log("Hello world!", out=out)
        result = out.getvalue().strip()

        self.assertTrue(result.endswith("Hello world!"))

    def test_get_all_gh_languages(self):
        langs = ghtools.utils.get_all_gh_languages()

        self.assertTrue(len(langs) > 100)
        self.assertTrue('java' in langs)
