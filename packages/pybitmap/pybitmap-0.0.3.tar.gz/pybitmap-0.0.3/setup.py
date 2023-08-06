#!/usr/bin/python
#coding:utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pybitmap",
    packages=find_packages(),
    version='0.0.3',
    description="使用bitmap存储海量整型数据",
    long_description=long_description,
    author="ghostcat_kun",
    author_email='ghostcat_kun@163.com',
    url="https://github.com/Alucardmini/basic_algrithms/blob/master/Bit_maps.py",
    download_url='https://github.com/Alucardmini/basic_algrithms/blob/master/Bit_maps.py',
    keywords=['bitmap', 'python', 'tool'],
    classifiers=[],
    entry_points={
        'console_scripts': [
        # 'command3 = adviserserver.run_algorithm:run'
    ]
    },
    install_requires=[

    ]
)
