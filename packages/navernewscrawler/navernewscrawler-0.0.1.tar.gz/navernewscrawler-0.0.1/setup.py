#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

setup(
    name='navernewscrawler',
    version='0.0.1',
    description='Tool for crawling news on Naver',
    url='',
    author=['Eunhou Esther Song'],
    author_email='eunhou.song@gmail.com',
    license='MIT',
    packages=find_packages(exclude=["build.*", "tests", "tests.*"]),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "navernewscrawler = navernewscrawler.main:main"
        ]
    })
