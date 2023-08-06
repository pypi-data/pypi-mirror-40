# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='taskprocessor',
    version='0.0.1',
    py_modules=['taskprocessor'],
    url='',
    license='MIT',
    description='Distributed task processing',
    install_requires=[
        'numpy',
        'pika>=0.12.0,<1',
        'dill>=0.2,<1',
    ],
    extras_require={
    },
)
