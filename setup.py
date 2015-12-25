#!/usr/bin/env python
from codecs import open

from setuptools import setup, find_packages

setup(
        name='gh-tools',
        version='0.2.5',
        description=('Collection of command line tools written in Python for ' +
                     'GitHub exploration and data mining.'),
        long_description=open('README.rst').read(),
        url='https://github.com/robvanderleek/gh-tools',
        author='Rob van der Leek',
        author_email='robvanderleek@gmail.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],
        keywords='sample setuptools development',
        packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
        install_requires=[
            'sh>=1.11'
        ],
        extras_require={},
        package_data={'ghtools': ['languages.yml']},
        data_files=[],
        scripts=['bin/gt-repo-query', 'bin/gt-repo-clone', 'bin/gt-repo-xargs'],
        # To provide executable scripts, use entry points in preference to the
        # "scripts" keyword. Entry points provide cross-platform support and allow
        # pip to create the appropriate form of executable for the target platform.
        # entry_points={
        #     'console_scripts': [
        #         'sample=sample:main',
        #     ],
        # },
)
