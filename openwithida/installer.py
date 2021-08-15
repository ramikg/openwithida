import argparse
import os
import re
import sys
try:
    import winreg  # Python 3
except ImportError:
    import _winreg as winreg  # Python 2
from distutils.version import StrictVersion

from openwithida import config

PYTHONW_EXE = 'pythonw.exe'
# The access key is 'w' as the other letters are taken by Windows/popular enough software
OPEN_WITH_IDA_VERB = 'Open &with IDA'


class OpenWithIdaInstallerIllegalIdaFolderError(Exception):
    pass


class OpenWithIdaInstallerFileDoesNotExistError(Exception):
    pass


class OpenWithIdaInstallerIdaNotFoundError(Exception):
    pass


def _legal_ida_folder(path):
    if not os.path.exists(path):
        raise OpenWithIdaInstallerIllegalIdaFolderError(
            '{} doesn\'t exist!'.format(path))

    ida_32_path = os.path.join(path, config.ida_32_exe)
    if not os.path.exists(ida_32_path):
        raise OpenWithIdaInstallerIllegalIdaFolderError(
            '{} not in folder'.format(config.ida_32_exe))

    ida_64_path = os.path.join(path, config.ida_64_exe)
    if not os.path.exists(ida_64_path):
        raise OpenWithIdaInstallerIllegalIdaFolderError(
            '{} not in folder'.format(config.ida_64_exe))

    return path


def _get_newest_ida_folder():
    highest_version = '0.0'
    newest_ida_folder = None

    for entry in os.listdir(config.program_files_folder):
        entry_path = os.path.join(config.program_files_folder, entry)

        if not os.path.isdir(entry_path):
            continue

        match = re.match(r'IDA Pro ([\d.]+)$', entry)
        if match:
            version = StrictVersion(match.group(1))
            if version > highest_version:
                highest_version = version
                newest_ida_folder = entry_path

    if not newest_ida_folder:
        raise OpenWithIdaInstallerIdaNotFoundError(
            'IDA folder not found in {}. Please specify manually.'.format(
                config.program_files_folder))

    return newest_ida_folder


def _get_pythonw_path():
    python_folder = os.path.dirname(sys.executable)

    pythonw_path = os.path.join(python_folder, PYTHONW_EXE)
    if not os.path.exists(pythonw_path):
        raise OpenWithIdaInstallerFileDoesNotExistError('{} doesn\'t exist'.format(pythonw_path))

    return pythonw_path


def _parse_args():
    parser = argparse.ArgumentParser(description='Install the OpenWithIDA context menu item.')

    parser.add_argument('--ida-folder', type=_legal_ida_folder, default=_get_newest_ida_folder(),
                        help='IDA installation folder. '
                             'Defaults to the newest IDA in "{}".'.format(
                                 config.program_files_folder))
    parser.add_argument('--pythonw-path', default=_get_pythonw_path(),
                        help='Path to pythonw.exe. '
                             'Defaults to the version you\'re running right now.')

    return parser.parse_args()


def install_openwithida(ida_folder=_get_newest_ida_folder(), pythonw_path=_get_pythonw_path()):
    command = r'"{pythonw_path}" -m {package_name} "%1"'.format(
        pythonw_path=pythonw_path,
        package_name=config.package_name)
    ida_exe_path = os.path.join(ida_folder, config.ida_32_exe)

    # Create "shell" registry key if doesn't exist
    with winreg.CreateKey(config.registry_root_key, config.registry_key) as _:
        pass

    openwithida_registry_key = '{}\\{}'.format(config.registry_key, config.registry_subkey)
    with winreg.CreateKey(config.registry_root_key, openwithida_registry_key) as hkey:
        # Set the "(Default)" value
        winreg.SetValue(hkey, None, winreg.REG_SZ, OPEN_WITH_IDA_VERB)
        winreg.SetValueEx(hkey, 'Icon', None, winreg.REG_SZ, ida_exe_path)
        with winreg.CreateKey(hkey, 'command') as command_hkey:
            winreg.SetValue(command_hkey, None, winreg.REG_SZ, command)


if __name__ == '__main__':
    args = _parse_args()

    install_openwithida(args.ida_folder, args.pythonw_path)
