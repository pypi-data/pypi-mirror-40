#!/usr/bin/env python
# symlinkator 0.1 - Find if a link linked to exist
# Author: Run Zhang
#
try:
  from setuptools import setup,find_packages
except:
  from ez_setup import use_setuptools
  use_setuptools()
  from setuptools import setup,find_packages
import os,sys

version = '0.1.4.2'
#f  = open(os.path.join(os.path.dirname(__file__),'docs','index.txt'))
#long_description = f.read().strip()
#f.close()

setup(
     name = "symlinkator",
     version = "0.2",
     packages = find_packages(),
     description = 'link checking tool',
     #long_description = long_description,
     classifiers = [
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: MIT License',
             ],
     author = 'Run Zhang',
     author_email = 'run.zhang@exeloncorp.com',
     url = 'http://unixportal.exelonds.com/linkator',
     download_url = 'http://unixportal.exelonds.com/idownload/linkator',
     license = 'MIT',
     py_modules =  ['virtualenv'],
     entry_points = {
         'console_scripts': [
            'linkator = symlinkator.symlinkator:main',
          ],
      },

)
