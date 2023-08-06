# -*- coding: UTF-8 -*-
"""
Client library for use with the weevils.io API
"""
from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md').read() + "\n" + open('CHANGELOG.md').read()

setup(
    name='weevils',
    author='weevils.io',
    author_email='code@weevils.io',
    description='A client library for using the weevils.io API',
    long_description=LONG_DESCRIPTION,
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests==2.21.0'],
    extras_require={
        'for_tests': ['nose==1.3.7'],
    },
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['weevils', 'api', 'client'],
    zip_safe=False,
)
