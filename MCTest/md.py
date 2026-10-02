import os
import sys

from tools import convert, commondata


class mod(sys.modules[__name__].__class__):
    def __call__(self, version, edition = 'pc'):
        '''_dir = os.path.join(
            os.path.dirname(__file__), "data/data/"
        )'''
        _dir = 'data/data/'
        return type(version, (object,), convert(_dir, version, edition))

    def common(self, edition = 'pc'):
        '''_dir = os.path.join(
            os.path.dirname(__file__), "data/data/"
        )'''
        _dir = 'data/data/'
        return type('common', (object,), commondata(_dir, edition))


sys.modules[__name__].__class__ = mod
