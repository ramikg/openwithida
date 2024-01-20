> [!NOTE]
> With the release of IDA 8.3, IDA32 has been deprecated, and this extension is no longer required.

# OpenWithIDA

Add "Open with IDA" to your Windows context menu.

_OpenWithIDA_ efficiently determines a file's bitness, and proceeds to open it using the correct (32-bit or 64-bit) variant of IDA.

![Screenshot](resources/screenshot.png)

## Installation

```batch
pip install openwithida
```

You should now have _OpenWithIDA_ installed using the latest IDA version found on your PC.  
If not automatically found, you will be prompted to choose your IDA folder.

## FAQ

### I've upgraded IDA. How to make _OpenWithIDA_ point to the newer version?

If you've completely uninstalled the previous version of IDA, the upgrade should be picked up automatically the next time you click "Open with IDA".

If the old version still exists, simply run

```batch
pip install --force-reinstall openwithida
```

### The context menu item wasn't installed

To find out the cause for the error, run `pip install` with the `-v` flag.

Alternatively, run the installer manually (see below).

### How to run the installer manually?

Manually invoking the installer offers the following additional options:

- Installing using a custom path for IDA or Python
- Installing as an extended verb (meaning you have to hold Shift to display it)
- Using IDA32 even in IDA 8.2+ (when applicable)
- Uninstalling the context menu extension

For usage information, run

```batch
python installer.py --help
```

(Even when `pip install` fails to install the context menu extension, `installer.py` should be available in the package's installation folder.)
