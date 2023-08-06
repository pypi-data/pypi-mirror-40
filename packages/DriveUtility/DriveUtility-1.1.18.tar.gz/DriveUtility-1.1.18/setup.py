# !/usr/bin/env python
# -*- coding: utf-8 -*-

#
#
# Copyright (c) 2018 Pedro Gabaldon
#
#
# Licensed under MIT License. See LICENSE
#
#

import setuptools
import platform

requires=["oauth2client", "httplib2", "google-api-python-client"]

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
	name="DriveUtility",
	version="1.1.18",
	author="Pedro Gabaldon Julia",
	author_email="petergj@protonmail.com",
	description="Google Drive tool",
	long_description=long_description,
    long_description_content_type="text/markdown",
	url="https://github.com/PeterGabaldon/DriveUtility",
	entry_points ={'console_scripts' : ['DriveUtil = DriveUtility.bin.DriveUtil:main']},
	license="MIT",
	install_requires=requires,
	packages=setuptools.find_packages(),
	include_package_data=True,
	classifiers=(
		"Programming Language :: Python :: 2.7",
		"License :: OSI Approved :: MIT License",
		"Development Status :: 4 - Beta",
		)

	)