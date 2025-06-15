#!/usr/bin/env python

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lsub-v1',
    version='1.0.0',
    description='Enhanced Subdomain Enumeration Tool with Improved crt.sh Integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/lsub-v1',
    license='MIT',
    py_modules=['lsub'],
    install_requires=[
        'requests>=2.25.1',
        'dnspython>=2.1.0',
    ],
    extras_require={
        'bruteforce': ['subbrute'],
    },
    entry_points={
        'console_scripts': [
            'lsub=lsub:interactive',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: System :: Networking',
    ],
    keywords='subdomain enumeration security penetration-testing reconnaissance',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/lsub-v1/issues',
        'Source': 'https://github.com/yourusername/lsub-v1',
        'Documentation': 'https://github.com/yourusername/lsub-v1/wiki',
    },
)
