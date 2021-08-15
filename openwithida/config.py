import winreg

package_name = 'openwithida'
registry_root_key = winreg.HKEY_CURRENT_USER
registry_key = r'SOFTWARE\Classes\*\shell'
registry_subkey = 'OpenWithIDA'
program_files_folder = r'C:\Program Files'
ida_32_exe = 'ida.exe'
ida_64_exe = 'ida64.exe'
