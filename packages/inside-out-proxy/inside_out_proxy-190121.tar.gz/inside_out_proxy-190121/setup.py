#!/usr/bin/env python
# coding: utf-8

import os, sys
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'README.md')) as fd:
    md = fd.read()

with open(os.path.join(HERE, 'src/inside_out_proxy/version.py')) as fd:
    version = fd.read().split('=', 1)[1].split('\n', 1)[0].strip()

# images hack for pypi - uncomment, replace:
# gh = 'https://raw.githubusercontent.com/axiros/terminal_markdown_viewer/master'
# md = md.replace('src="./', 'src="%s/' % gh)

PY2 = sys.version_info[0] < 3
INST_REQ = [
    'attrs',
    'structlog',
    'attrs',
    'colorama',
    'pygments',
    'absl-py',
    'appdirs',
    'rx',
    'gevent',
]

EXTRA_REQ = {'tests': ['coverage', 'pytest_to_md', 'pytest>=3.3.0']}
PACKAGES = find_packages(where='src', exclude=['inside_out_proxy.egg_info'])


setup(
    name='inside_out_proxy',
    version=version,
    packages=PACKAGES,
    package_dir={'': 'src'},
    author='Axiros GmbH',
    author_email='gk@axiros.com',
    description='HTTP Proxy',
    install_requires=INST_REQ,
    extras_require=EXTRA_REQ,
    long_description=md,
    long_description_content_type='text/markdown',
    include_package_data=True,
    # url='http://github.com/axiros/inside_out_proxy',
    # download_url='http://github.com/axiros/inside_out_proxy/tarball/',
    keywords=['http', 'proxy'],
    # test_suite='nose.collector',
    # tests_require=['nose', 'unittest2', 'coveralls'],
    # better than entrypoints for cflags --help:
    scripts=[
        'src/inside_out_proxy/inside_out_proxy',
        'src/inside_out_proxy/inside_out_proxy_test_jobserver',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Topic :: Internet :: Proxy Servers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
)
