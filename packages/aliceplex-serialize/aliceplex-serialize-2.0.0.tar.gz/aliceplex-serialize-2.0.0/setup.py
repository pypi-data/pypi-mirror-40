from setuptools import find_namespace_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(name="aliceplex-serialize",
      version="2.0.0",
      author="Alice Plex",
      url="https://gitlab.com/alice-plex/serialize",
      description="Serialization library for Plex",
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires=">=3.7",
      packages=find_namespace_packages(include=["aliceplex.*"]),
      install_requires=[
          "aliceplex-schema>=3.0.2,<4.0.0",
          "marshmallow>=3.0.0b20,<4.0.0",
          "ruamel.yaml>=0.15.61"
      ],
      classifiers=(
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent"
      ))
