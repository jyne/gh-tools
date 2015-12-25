from unittest import TestCase

import ghtools.utils

class utilsTest(TestCase):
    def test_get_all_gh_languages(self):
        langs = ghtools.utils.get_all_gh_languages()

        self.assertTrue(len(langs) > 100)
        self.assertTrue('java' in langs)