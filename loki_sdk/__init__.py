#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loki SDK for Python
"""

from .loki_sdk import (
    LokiSDK,
    get_sdk,
    init_sdk,
    log,
    debug,
    info,
    warning,
    error,
    critical,
    flush,
)

__version__ = "1.0.0"
__author__ = "ppyuesheng"
__email__ = "ppyuesheng@hotmail.com"

__all__ = [
    "LokiSDK",
    "get_sdk",
    "init_sdk",
    "log",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "flush",
]
