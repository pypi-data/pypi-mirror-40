# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

from setuptools import find_packages, setup

import io

with io.open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(name="ttn",
      version="2.1.5",
      description="The Things Network Client",
      long_description = long_description,
      url = "https://github.com/TheThingsNetwork/python-app-sdk",
      author="Johan Stokking",
      author_email="johan@thethingsnetwork.org",
      license="MIT",
      packages=find_packages(),
      install_requires=[
          "paho-mqtt",
          "events",
          "grpcio",
          # packages which need to be imported to make gRPC work
          "protobuf",
          "googleapis-common-protos"
      ],
      zip_safe=False)
