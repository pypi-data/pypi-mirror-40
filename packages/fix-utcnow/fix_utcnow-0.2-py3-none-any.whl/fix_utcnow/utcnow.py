# coding: utf-8
import inspect
import os
from ctypes import *

cur_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

libc = CDLL(os.path.join(cur_path, 'c/libfixutcnow.so'))
_fix_utcnow = libc.utcnow
_fix_utcnow.restype = c_char_p


def fix_utcnow():
    return _fix_utcnow().decode()
