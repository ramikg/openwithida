import atexit
import os
from setuptools import setup, find_packages
from setuptools.command.install import install

from openwithida import config
from openwithida import installer

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path) as readme:
    long_description = readme.read()


class PostInstallHook(install, object):
    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        atexit.register(installer.install_openwithida)


setup(name=config.package_name,
      description='Right click -> "Open with IDA"',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ramikg/openwithida',
      version='0.4.0',
      packages=find_packages(),
      install_requires=['bitnesslib>=0.1.2'],
      classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows'
      ],
      cmdclass={
        'install': PostInstallHook
      })
