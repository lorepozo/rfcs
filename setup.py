#!/usr/bin/env python

from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='rfcs',
    version=version,
    description='rfcs is the complete command-line tool to search and view RFCs.',
    long_description=open('README.rst').read(),
    author='Lucas Morales',
    author_email='lucas@lucasem.com',
    license='GNU GPL v2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Communications',
        'Topic :: Documentation',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: Software Development :: Documentation',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    keywords='rfc internet networking protocol concept notes command command-line cli',
    url='http://github.com/lukedmor/rfcs',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests'],
    entry_points={
        'console_scripts': [
            rfcs=rfcs.rfcs:main
        ],
    }
)
