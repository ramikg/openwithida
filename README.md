# OpenWithIDA

Add "Open With IDA" to your Windows context menu.

_OpenWithIDA_ efficiently determines a file's bitness, and proceeds to open it using the correct (32-bit or 64-bit) variant of IDA.

![Screenshot](resources/screenshot.png)

## Installation

```batch
pip install openwithida
```

You should now have _OpenWithIDA_ installed using the latest IDA version found on your PC.

## FAQ

### The context menu item wasn't installed

To find out the cause for the error, run `pip install` with the `-v` flag.

The cause is most likely a nonstandard IDA folder location, and the solution is to run the installer manually (see below).

### How to install the _OpenWithIDA_ context menu extension manually?

If the automatic `pip install` installation failed, or if you want to use a custom path for IDA or Python, you may manually (re)install the context menu item:

```batch
python installer.py --help
```

(Even when `pip install` fails to install the context menu extension, `installer.py` should be available in the package's installation folder.)
