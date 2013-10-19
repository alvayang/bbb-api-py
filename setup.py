#!/usr/bin/env python


from setuptools import setup

version = '0.0.1'

setup(name='bbbapi',
        version=version,
        author='Yang.Song',
        author_email='alvayang@programmer.sh',
        description='A very simple python wrapper for bigbluebutton',
        url='https://github.com/alvayang/bbb-api-py',
        packages=['bbbapi'],
        include_package_data=False,
        zip_safe=True,
        license='https://github.com/alvayang/bbb-api-py/blob/master/LICENSE',
        )
