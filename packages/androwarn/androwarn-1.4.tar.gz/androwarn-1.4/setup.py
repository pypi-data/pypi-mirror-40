#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='androwarn',
      version='1.4',
      description='Yet another static code analyzer for malicious Android applications',
      long_description_content_type='text/markdown; charset=UTF-8;',
      long_description=open('androwarn/README.md').read(),
      url='https://github.com/maaaaz/androwarn',
      author='Thomas D.',
      author_email='tdebize@mail.com',
      license='LGPL',
      classifiers=[
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
      ],
      keywords='androwarn android apk dalvik static malicious behaviours behaviors reverse disassemble',
      packages=find_packages(),
      install_requires=['argparse', 'androguard >= 3.2.1', 'jinja2', 'play_scraper'],
      python_requires='<3, >2.6',
      entry_points = {
        'console_scripts': ['androwarn=androwarn.androwarn:main'],
      },
      include_package_data=True)