# -*- coding: utf-8 -*-
"""
socketio-client
----------------------

Socket.IO client.
"""
from setuptools import setup

setup(
    name='fourdrop-socketio-client',
    version='1.1',
    url='http://github.com/PeterWunderlich/python-socketio-client/',
    license='MIT',
    author='Peter Wunderlich',
    author_email='wunderlich.p@outlook.com',
    description='Socket.IO client',
    long_description=open('README.rst').read(),
    packages=['socketio_client'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'engineio-client>=0.2',
        'gevent>=1.0.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

