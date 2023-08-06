__version__ = '0.1'
__author__ = 'Taehong Kim'
__email__ = 'peppy0510@hotmail.com'
__license__ = 'BSD'
__doc__ = '''
bass_module, func_type = bass.load(__file__)
'''


import ctypes
import os
import platform
import sys


def load(name='bass'):
    name = os.path.splitext(os.path.basename(name))[0]
    if name.startswith('py'):
        name = name[2:]
    lib = os.path.join(os.path.dirname(__file__), 'lib')
    architecture = 'x64' if platform.machine().endswith('64') else 'x86'
    extension = ['', '.dll'] if sys.platform.startswith('win') else ['lib', '.so']
    filename = name.join(extension)
    path = os.path.join(lib, architecture, filename)

    if os.path.isfile(path):
        try:
            if sys.platform.startswith('win'):
                bass_module = ctypes.WinDLL(path)
                func_type = ctypes.WINFUNCTYPE
            else:
                bass_module = ctypes.CDLL(path, mode=ctypes.RTLD_GLOBAL)
                func_type = ctypes.CFUNCTYPE
            return bass_module, func_type
        except Exception:
            pass
    raise FileNotFoundError('Failed to load BASS module "%s"' % (filename))


if __name__ == '__main__':
    bass_module, func_type = load('bass')
