#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup script for rpi-cam-mqtt."""

from setuptools import setup
import io

version='0.9.4'

setup(
    name="rpicammqtt",
    version=version,
    packages=['rpicammqtt'],
    install_requires=['PyYaml>=3.12', 'paho-mqtt>=1.4.0', 'adafruit-pca9685'],
    include_package_data=True,

    # metadata
    author="Gianluca Busiello",
    author_email="gianluca.busiello@gmail.com",
    description="Mqtt agent for rpi-cam-web-interface",
    long_description=io.open('README.md', 'r', encoding="UTF-8").read(),
    url="https://gitlab.com/gbus/rpi-cam-mqtt",
    entry_points = {
        'console_scripts': [
            'rpicammqtt = rpicammqtt.__main__:main',
            'configpt = rpicammqtt.configpt:main'
        ],
    },
    package_data={
        'rpicammqtt': ['data/*.json', 'config/*.yaml', 'systemd/rpi-cam-mqtt.service'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    zip_safe=False
)
