# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='msspec',
    packages=find_packages(),
    version='0.0.1',
    description='A simple module for basic mass-spectra operations.',
    long_description='A simple module for basic mass-spectra opertations.',
    author=u'Mateusz Krzysztof Łącki',
    author_email='matteo.lacki@gmail.com',
    url='https://github.com/MatteoLacki/massspectrum',
    # download_url='https://github.com/MatteoLacki/MassTodonPy/tree/GutenTag',
    keywords=[
        'Analitical Chemistry',
        'Mass Spectrometry'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6'],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
    ]
    # scripts=[
    #     'bin/rtc']
)
