# coding: utf-8
import inspect
import os
from ctypes import *

import pkg_resources

cur_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
libc = CDLL(pkg_resources.resource_filename(pkg_resources.Requirement.parse('fix_utcnow'), 'c/libfixutcnow.so'))
# libc = CDLL(os.path.join(cur_path, 'c/libfixutcnow.so'))
_fix_utcnow = libc.utcnow
_fix_utcnow.restype = c_char_p


def fix_utcnow():
    return _fix_utcnow().decode()
