#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

__author__ = "Eric Busboom"
__copyright__ = "Eric Busboom"
__license__ = "mit"

import logging
import json
from dtcv.download import logger as download_logger

#download_logger.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

def test_fib():
    from dtcv.counts import extract_count_annotations

    df = intersections_df()

    print(df.head().T)