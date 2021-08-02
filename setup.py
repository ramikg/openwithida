import atexit
from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path

from openwithida import config
from openwithida import installer

readme_path = Path(__file__).parent / 'README.md'
PACKAGE_NAME = 'openwithida'


class OpenWithIdaPostInstallHookError(Exception):
    pass


# Disabling bdist_wheel ensures the install command's self.install_lib
# will point to the correct site-packages directory.
WheelDisableHook = None
try:
    from wheel.bdist_wheel import bdist_wheel

    class WheelDisableHook(bdist_wheel):
        def run(self, *args, **kwargs):
            return
except ModuleNotFoundError:
    pass


class PostInstallHook(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(self._post_install)

    def _post_install(self):
        openwithida_path = Path(self.install_lib) / PACKAGE_NAME / config.openwithida_py
        if not openwithida_path.exists():
            raise OpenWithIdaPostInstallHookError(f'{openwithida_path} doesn\'t exist')
        print(f'Found {config.openwithida_py}: {openwithida_path}')

        installer.install_openwithida(openwithida_path=openwithida_path)


setup(name=PACKAGE_NAME,
      description='Right click -> "Open with IDA"',
      long_description=readme_path.read_text(),
      long_description_content_type="text/markdown",
      url='https://github.com/ramikg/openwithida',
      version='0.1',
      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=['bitnesslib'],
      classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Microsoft :: Windows"
      ],
      cmdclass={
        'bdist_wheel': WheelDisableHook,
        'install': PostInstallHook
      })
