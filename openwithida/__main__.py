import argparse
import os
import subprocess
try:
    import winreg  # Python 3
except ImportError:
    import _winreg as winreg  # Python 2

import bitnesslib

from openwithida import common
from openwithida import config
from openwithida import installer

SUBPROCESS_DETACHED_PROCESS = 0x00000008


class OpenWithIdaInvalidIdaBitnessError(Exception):
    pass


class OpenWithIdaNotInstalledError(Exception):
    pass


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='Input file path.')

    parser.add_argument('--use-ida32', action='store_true', help='Use IDA32 even in IDA 8.2+')

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


def _choose_ida_bitness(ida_folder, input_path, use_ida32):
    FALLBACK_IDA_BITNESS = 32  # Relevant only for versions < 8.2

    if not use_ida32:
        ida_version = common.ida_folder_name_to_version_tuple(ida_folder)
        if ida_version >= (8, 3):
            return 64
        if ida_version == (8, 2):
            return 32 if input_path.endswith('.idb') else 64

    try:
        file_bitness = bitnesslib.get_bitness(input_path)
    except bitnesslib.BitnessLibUnknownFormatError:
        # We'd still like to open the file using some IDA
        file_bitness = FALLBACK_IDA_BITNESS
    
    if file_bitness in (32, 64):
        return file_bitness
    else:
        return FALLBACK_IDA_BITNESS


def open_with_ida(ida_folder, input_path, use_ida32):
    ida_bitness = _choose_ida_bitness(ida_folder, input_path, use_ida32)

    if ida_bitness == 64:
        ida_64_path = os.path.join(ida_folder, config.ida_64_exe)
        _create_detached_process(ida_64_path, input_path)
    elif ida_bitness == 32:
        ida_32_path = os.path.join(ida_folder, config.ida_32_exe)
        _create_detached_process(ida_32_path, input_path)
    else:
        raise OpenWithIdaInvalidIdaBitnessError(ida_bitness)


if __name__ == '__main__':
    args = _parse_args()

    ida_folder = _get_ida_folder()
    if not os.path.isdir(ida_folder):
        # Perhaps the IDA folder was deleted in favour of a newer version.
        installer.install_openwithida()
        ida_folder = _get_ida_folder()

    open_with_ida(ida_folder, args.path, args.use_ida32)
