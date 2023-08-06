# coding=utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yingjia_common",
    version="1.0.4",
    author="RobinSun",
    author_email="xiaoshousoft@163.com",
    description="赢家公共包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://39.106.175.106:81/svn/yj_server/src/common/trunk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


# python setup.py sdist bdist_wheel
# set path=C:\Users\25731\AppData\Roaming\Python\Python36\Scripts
# twine upload dist/*
# xiaoshousoft Robin19890425