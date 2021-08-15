import atexit
from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path

from openwithida import config
from openwithida import installer

readme_path = Path(__file__).parent / 'README.md'


class PostInstallHook(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(installer.install_openwithida)


setup(name=config.package_name,
      description='Right click -> "Open with IDA"',
      long_description=readme_path.read_text(),
      long_description_content_type='text/markdown',
      url='https://github.com/ramikg/openwithida',
      version='0.1.1',
      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=['bitnesslib'],
      classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows'
      ],
      cmdclass={
        'install': PostInstallHook
      })
