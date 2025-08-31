#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# 读取requirements文件
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="loki-sdk-py",
    version="1.0.0",
    author="ppyuesheng",
    author_email="ppyuesheng@hotmail.com",
    description="A Python SDK for sending logs to Loki server, based on python-logging-loki",
    long_description=read_readme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/ppyuesheng-org/loki-sdk-py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    keywords="loki, logging, sdk, python, grafana",
    project_urls={
        "Bug Reports": "https://github.com/ppyuesheng-org/loki-sdk-py/issues",
        "Source": "https://github.com/ppyuesheng-org/loki-sdk-py",
        "Documentation": "https://github.com/ppyuesheng-org/loki-sdk-py#readme",
    },
)
