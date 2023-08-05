#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = ["coverage", "flake8", "wheel"]

setup(
    name="gcpcli",
    version="0.0.1",
    url="https://github.com/kislyuk/gcp-cli",
    license="Apache Software License",
    author="Andrey Kislyuk",
    author_email="kislyuk@gmail.com",
    description="GCP CLI",
    long_description=open("README.rst").read(),
    install_requires=[
    ],
    tests_require=tests_require,
    extras_require={"test": tests_require},
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
#            'tq=yq:tq_cli'
        ],
    },
    test_suite="test",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
