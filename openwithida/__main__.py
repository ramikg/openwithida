import argparse
import os
import subprocess
try:
    import winreg  # Python 3
except ImportError:
    import _winreg as winreg  # Python 2

import bitnesslib

from openwithida import config

SUBPROCESS_DETACHED_PROCESS = 0x00000008


class OpenWithIdaNotInstalledError(Exception):
    pass


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='Input file path.')

    return parser.parse_args()


def _create_detached_process(ida_path, input_path):
    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | SUBPROCESS_DETACHED_PROCESS
    subprocess.Popen([ida_path, input_path],
                     creationflags=creation_flags,
                     close_fds=True)


def _get_ida_folder():
    registry_key = '{}\\{}'.format(config.registry_key, config.registry_subkey)
    try:
        with winreg.OpenKey(config.registry_root_key, registry_key) as hkey:
            ida_exe_path = winreg.QueryValueEx(hkey, 'Icon')[0]
            return os.path.dirname(ida_exe_path)
    except WindowsError:
        raise OpenWithIdaNotInstalledError('Please run installer.py')


def open_with_ida(ida_folder, input_path):
    try:
        file_bitness = bitnesslib.get_bitness(input_path)
    except bitnesslib.BitnessLibUnknownFormatError:
        # We'd still like to open the file using some IDA
        file_bitness = None

    if file_bitness == 64:
        ida_64_path = os.path.join(ida_folder, config.ida_64_exe)
        _create_detached_process(ida_64_path, input_path)
    else:
        ida_32_path = os.path.join(ida_folder, config.ida_32_exe)
        _create_detached_process(ida_32_path, input_path)


if __name__ == '__main__':
    args = _parse_args()

    ida_folder = _get_ida_folder()

    open_with_ida(ida_folder, args.path)
