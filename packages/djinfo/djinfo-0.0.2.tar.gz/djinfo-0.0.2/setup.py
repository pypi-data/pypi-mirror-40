# -*- coding: utf-8 -*-
"""
EmailHub setup file
"""
import io
import os

from setuptools import setup, find_packages

PACKAGE_NAME, VERSION = ('djinfo', '__version__')
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_PATH = os.path.join(ROOT_PATH, PACKAGE_NAME)

with io.open(os.path.join(PACKAGE_PATH, VERSION)) as f:
    VERSION = f.readline().strip()

    with io.open(os.path.join(ROOT_PATH, 'README.rst'), encoding='utf8') as f:
        README = f.read()

        setup(
            name=PACKAGE_NAME,
            version=VERSION,
            description='Django system information page, suitable for production',  # noqa
            long_description=README,
            author='Maxime Haineault',
            author_email='haineault@gmail.com',
            license='MIT',
            url='https://gitlab.com/h3/djinfo',
            packages=find_packages(),
            include_package_data=True,
            zip_safe=True,
            install_requires=[
                'Django>=1.8',
                'six>=1.11.0',
            ],
            extras_require={
                'tests': [
                    'tox>=3.6',
                    'detox>=0.18',
                ],
                'docs': [
                    'Sphinx==1.7.1',
                    'sphinxcontrib-napoleon==0.6.1',
                    'sphinx-rtd-theme==0.4.2',
                    'docutils==0.12',
                ]
            },
            classifiers=[
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
            ]
        )
