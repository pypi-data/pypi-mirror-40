#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@project: crawl img tag source
@author: xiaohong
@time: 2019-01-01
@feature: crawl image for every site/multi thread to download/
"""

import setuptools

with open("crawl_image/README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawl_image",
    version="0.0.3",

    author="xiaohong2019",
    author_email="2229009854@qq.com",

    description="crawl web image source",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/xiaohong2019/crawl_image",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)