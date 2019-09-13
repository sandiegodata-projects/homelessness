#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

__author__ = "Eric Busboom"
__copyright__ = "Eric Busboom"
__license__ = "mit"

import logging
import json
from dtcv.download import logger as download_logger
from dtcv.counts import get_count_files, load_count_rows, count_df, file_df

#download_logger.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

def test_fib():

    df = file_df();
    print(df.head())