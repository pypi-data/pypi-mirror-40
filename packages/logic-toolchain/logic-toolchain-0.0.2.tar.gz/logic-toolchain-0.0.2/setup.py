#!/usr/bin/env python3
#
# Copyright 2019 Tymoteusz Blazejczyk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

def readme():
    text = str()
    with open('README.md', 'r') as f:
        text = f.read()
    return text

setup(
    name='logic-toolchain',
    version='v0.0.2',
    description='Wrapper for FPGA toolchain tools',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/tymonx/logic-toolchain',
    author='Tymoteusz Blazejczyk',
    author_email='tymoteusz.blazejczyk.pl@gmail.com',
    license='Apache 2.0',
    keywords=[
        'verilog',
        'vhdl',
        'fpga',
        'hdl',
        'rtl'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Compilers',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ]
)
