import argparse
import os
import re
import sys
import winreg
from pathlib import Path
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
    path = Path(path)

    if not path.exists():
        raise OpenWithIdaInstallerIllegalIdaFolderError(f'{path} doesn\'t exist!')

    if not (path / config.ida_32_exe).exists():
        raise OpenWithIdaInstallerIllegalIdaFolderError(f'{config.ida_32_exe} not in folder')

    if not (path / config.ida_64_exe).exists():
        raise OpenWithIdaInstallerIllegalIdaFolderError(f'{config.ida_64_exe} not in folder')

    return path


def _get_newest_ida_folder():
    highest_version = '0.0'
    newest_ida_folder = None

    with os.scandir(config.program_files_folder) as iterator:
        for entry in iterator:
            match = re.match(r'IDA Pro ([\d.]+)$', entry.name)
            if match:
                version = StrictVersion(match.group(1))
                if version > highest_version:
                    highest_version = version
                    newest_ida_folder = entry.path

    if not newest_ida_folder:
        raise OpenWithIdaInstallerIdaNotFoundError(
            f'IDA folder not found in {config.program_files_folder}. Please specify manually.')

    return newest_ida_folder


def _get_pythonw_path():
    python_folder = Path(sys.executable).parent

    pythonw_path = python_folder / PYTHONW_EXE
    if not pythonw_path.exists():
        raise OpenWithIdaInstallerFileDoesNotExistError(f'{pythonw_path} doesn\'t exist')

    return pythonw_path


def _parse_args():
    parser = argparse.ArgumentParser(description='Install the OpenWithIDA context menu item.')

    parser.add_argument('--ida-folder', type=_legal_ida_folder, default=_get_newest_ida_folder(),
                        help='IDA installation folder. '
                             f'Defaults to the newest IDA in "{config.program_files_folder}".')
    parser.add_argument('--pythonw-path', default=_get_pythonw_path(),
                        help='Path to pythonw.exe. '
                             'Defaults to the version you\'re running right now.')

    return parser.parse_args()


def install_openwithida(ida_folder=_get_newest_ida_folder(), pythonw_path=_get_pythonw_path()):
    command = rf'"{pythonw_path}" -m {config.package_name} "%1"'
    exe_path = str(Path(ida_folder) / config.ida_32_exe)

    # Create "shell" registry key if doesn't exist
    with winreg.CreateKey(config.registry_root_key, config.registry_key) as _:
        pass

    openwithida_registry_key = '{}\\{}'.format(config.registry_key, config.registry_subkey)
    with winreg.CreateKey(config.registry_root_key, openwithida_registry_key) as hkey:
        # Set the "(Default)" value
        winreg.SetValue(hkey, None, winreg.REG_SZ, OPEN_WITH_IDA_VERB)
        winreg.SetValueEx(hkey, 'Icon', None, winreg.REG_SZ, exe_path)
        with winreg.CreateKey(hkey, 'command') as command_hkey:
            winreg.SetValue(command_hkey, None, winreg.REG_SZ, command)


if __name__ == '__main__':
    args = _parse_args()

    install_openwithida(args.ida_folder, args.pythonw_path)
