# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    name="music_story",
    version="0.1",
    packages=find_packages('.'),
    author="Kevin Samuel",
    author_email="kevin.samuel@yandex.com",
    description="Music Story Python SDK",
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=['docopt', 'pytest', 'requests-oauthlib'],
    classifiers=[
        'Programming Language :: Python',
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3"
    ],
    url="http://developers.music-story.com"
)

