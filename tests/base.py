import os
import sys
import unittest


class BaseTest(unittest.TestCase):
    @property
    def verbosity(self):
        # there is no verbosity for nosetest, this trick allows us to emulate
        # it
        return int(os.environ.get('TEST_VERBOSITY', 2))

    def display_ok(self):
        """Helper that depends on verbosity prints 'ok' or '.' this is to be
        used when we want to emulate behaviour or nosetest/unittest from inside
        of single test. Especially when you have long running test that
        generates hundreds of smaller tests.
        """
        if self.verbosity:
            print("ok")
        else:
            print(".", sep=' ', end='')

        sys.stdout.flush()

    def display_fail(self):
        if self.verbosity:
            print("FAIL")
        else:
            print("F", sep=' ', end='')

    def display_error(self):
        if self.verbosity:
            print("ERROR")
        else:
            print("E", sep=' ', end='')

        sys.stdout.flush()

    def display_skip(self):
        if self.verbosity:
            print("SKIP")
        else:
            print("S", sep=' ', end='')
