# OpenWithIDA

Adds "Open With IDA" to your Windows context menu.

_OpenWithIDA_ efficiently determines a file's bitness, and proceeds to open it using the correct (32-bit or 64-bit) variant of IDA.

![Screenshot](resources/screenshot.png)

## Requirements

- Python 3.6+ (doesn't have to be the version you're using for IDA)

## Installation

1. Move the project's source code to a folder of your choice.  
For example, to `%APPDATA%\Hex-Rays\IDA Pro\OpenWithIDA`.
2. In this folder, run

    ```bash
    pip install -Ur requirements.txt
    python installer.py
    ```

You will now have _OpenWithIDA_ installed using the latest IDA version found on your PC.

At any time in the future, you may reinstall _OpenWithIDA_ using different paths for IDA, Python & _OpenWithIDA_.  
(See `python installer.py --help` for the configuration options.)
