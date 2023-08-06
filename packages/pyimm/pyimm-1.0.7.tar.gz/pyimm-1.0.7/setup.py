'''
 Copyright (c) 2016, 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from setuptools import setup, find_packages

setup(name='pyimm',
      version='1.0.7',
      description='Python Program to read IMM data files from XPCS beamlines ' +
                'at the Advanced Photon Source',
      author = 'John Hammonds, Benjamin Pausma, Timothy Madden',
      author_email = 'JPHammonds@anl.gov',
      url = 'https://confluence.aps.anl.gov/',
      packages = find_packages() ,
      package_data = {'' : ['LICENSE',]},
      license = 'See LICENSE File',
      platforms = 'any',
      )
