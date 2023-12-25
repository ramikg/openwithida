import re


class OpenWithIdaCommonInvalidIdaFolderName(Exception):
    pass


def _version_string_to_tuple(version_string):
    version_parts = version_string.split('.')
    return tuple(map(int, version_parts))


def ida_folder_name_to_version_tuple(folder_name):
    match = re.search(r'IDA Pro ([\d.]+)$', folder_name)
    if match:
        return _version_string_to_tuple(match.group(1))
    else:
        raise OpenWithIdaCommonInvalidIdaFolderName(folder_name)
