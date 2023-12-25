import argparse
import os
import re
import sys
try:
    # Python 3
    import winreg
    import tkinter as tk
    import tkinter.filedialog as tk_filedialog
except ImportError:
    # Python 2
    import _winreg as winreg
    import Tkinter as tk
    import tkFileDialog as tk_filedialog


from openwithida import common
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


class OpenWithIdaInstallerUserCancelledPrompt(Exception):
    pass


def _verify_legal_ida_folder(path):
    if not os.path.isdir(path):
        raise OpenWithIdaInstallerIllegalIdaFolderError(
            '{} doesn\'t exist!'.format(path))

    ida_32_path = os.path.join(path, config.ida_32_exe)
    if not os.path.isfile(ida_32_path):
        raise OpenWithIdaInstallerIllegalIdaFolderError(
            '{} not in folder'.format(config.ida_32_exe))

    ida_64_path = os.path.join(path, config.ida_64_exe)
    if not os.path.isfile(ida_64_path):
        raise OpenWithIdaInstallerIllegalIdaFolderError(
            '{} not in folder'.format(config.ida_64_exe))

    return path


def _get_newest_ida_folder():
    highest_version = (0, 0)
    newest_ida_folder = None

    for entry in os.listdir(config.program_files_folder):
        entry_path = os.path.join(config.program_files_folder, entry)

        if not os.path.isdir(entry_path):
            continue

        try:
            version_tuple = common.ida_folder_name_to_version_tuple(entry)
            if version_tuple > highest_version:
                highest_version = version_tuple
                newest_ida_folder = entry_path
        except common.OpenWithIdaCommonInvalidIdaFolderName:
            continue

    if not newest_ida_folder:
        raise OpenWithIdaInstallerIdaNotFoundError()

    return newest_ida_folder


def _prompt_user_for_ida_folder():
    widget = tk.Tk()
    widget.withdraw()

    folder = tk_filedialog.askdirectory(
        mustexist=True,
        initialdir=config.program_files_folder,
        title='Please choose your IDA folder')

    if not folder:
        raise OpenWithIdaInstallerUserCancelledPrompt()

    return folder


def _get_ida_folder():
    try:
        return _get_newest_ida_folder()
    except OpenWithIdaInstallerIdaNotFoundError:
        return _prompt_user_for_ida_folder()


def _get_pythonw_path():
    python_folder = os.path.dirname(sys.executable)

    pythonw_path = os.path.join(python_folder, PYTHONW_EXE)
    if not os.path.isfile(pythonw_path):
        raise OpenWithIdaInstallerFileDoesNotExistError('{} doesn\'t exist'.format(pythonw_path))

    return pythonw_path


def _parse_args():
    parser = argparse.ArgumentParser(description='Install the OpenWithIDA context menu item.')

    parser.add_argument('--ida-folder',
                        type=_verify_legal_ida_folder,
                        help='IDA installation folder. '
                             'Defaults to the newest IDA in "{}".'.format(
                                 config.program_files_folder))
    parser.add_argument('--pythonw-path',
                        default=_get_pythonw_path(),
                        help='Path to pythonw.exe. '
                             'Defaults to the version you\'re running right now.')
    parser.add_argument('--extended-verb',
                        action='store_true',
                        help='Will require holding Shift to display the context menu item.')
    parser.add_argument('--use-ida32',
                        action='store_true',
                        help='Use IDA32 even in IDA 8.2+')
    parser.add_argument('--uninstall',
                        action='store_true',
                        help='Uninstall the OpenWithIDA context menu item.')

    return parser.parse_args()


def _get_openwith_registry_key():
    return '{}\\{}'.format(config.registry_key, config.registry_subkey)


def uninstall_openwithida():
    openwithida_registry_key = _get_openwith_registry_key()
    openwithida_command_registry_subkey = '{}\\{}'.format(openwithida_registry_key, 'command')

    winreg.DeleteKey(config.registry_root_key, openwithida_command_registry_subkey)
    winreg.DeleteKey(config.registry_root_key, openwithida_registry_key)


def install_openwithida(ida_folder=None, pythonw_path=None, extended_verb=False, use_ida32=False):
    # Lazily calculate default values
    ida_folder = ida_folder or _get_ida_folder()
    pythonw_path = pythonw_path or _get_pythonw_path()

    _verify_legal_ida_folder(ida_folder)

    command = r'"{pythonw_path}" -m {package_name} "%1"{use_ida32}'.format(
        pythonw_path=pythonw_path,
        package_name=config.package_name,
        use_ida32=' --use-ida32' if use_ida32 else '')
    ida_exe_path = os.path.join(ida_folder, config.ida_32_exe)

    # Create "shell" registry key if doesn't exist
    with winreg.CreateKey(config.registry_root_key, config.registry_key) as _:
        pass

    openwithida_registry_key = _get_openwith_registry_key()
    with winreg.CreateKey(config.registry_root_key, openwithida_registry_key) as hkey:
        # Set the "(Default)" value
        winreg.SetValue(hkey, None, winreg.REG_SZ, OPEN_WITH_IDA_VERB)
        if extended_verb:
            winreg.SetValueEx(hkey, 'Extended', None, winreg.REG_SZ, None)
        winreg.SetValueEx(hkey, 'Icon', None, winreg.REG_SZ, ida_exe_path)
        with winreg.CreateKey(hkey, 'command') as command_hkey:
            winreg.SetValue(command_hkey, None, winreg.REG_SZ, command)


if __name__ == '__main__':
    args = _parse_args()

    if args.uninstall:
        uninstall_openwithida()
    else:
        install_openwithida(args.ida_folder, args.pythonw_path, args.extended_verb, args.use_ida32)
