"""Download annocations for counts and prepare dataframes"""


from pathlib import Path
import json
from operator import itemgetter
import pandas as pd
import numpy as np
import logging
import urllib.request
from .download import download_to_file

from . import count_list_url

logger = logging.getLogger('count')


def get_count_files():
    '''Yield all images, downloading if necessary'''

    with urllib.request.urlopen(count_list_url) as response:
        for l in response.readlines():
            url = l.strip().decode('ascii')

            yield download_to_file(url)

def extract_region_annotations(o):
    pass

    reg_cols = 'Type count'.split()
    reg_ig = itemgetter(*reg_cols)

    shape_cols = 'cx cy r'.split()
    shape_ig = itemgetter(*shape_cols)

    d = o['_via_img_metadata']

    for k, v in d.items():
        if k == 'example':
            continue

        for region in v['regions']:
            try:

                cx, cy, r = list(shape_ig(region['shape_attributes']))
                typ, count = list(reg_ig(region['region_attributes']))

                o={'image_url':v['filename']}

                o.update({
                    'cx': cx,
                    'cy': cy,
                    'r': r,
                    'type': typ,
                    'count': count

                })

                yield o

            except KeyError as e:
                logger.error("Error. wrong keys in shape attributes: ", region['shape_attributes'])


def load_count_rows():

    rows = []

    headers = None

    for e in get_count_files():

        with e.open() as f:
            o = json.load(f)

            for a in extract_region_annotations(o):
                if headers is None:
                    headers = list(a.keys())

                rows.append(list(a.values()))

    return headers, rows


def count_df():

    headers, rows = load_count_rows()

    return pd.DataFrame(rows, columns=headers)


def extract_file_annotations(o):
    d = o['_via_img_metadata']

    file_cols = 'date neighborhood total_count temp rain '.split()

    def get_file_cols(d):
        row = {}
        for c in file_cols:
            row[c] = d.get(c)

        return row

    for k, v in d.items():
        if k == 'example':
            continue

        o={'image_url':v['filename']}
        o.update(get_file_cols(v['file_attributes']))

        yield o


def load_file_rows():

    rows = []

    headers = None

    for e in get_count_files():

        with e.open() as f:
            o = json.load(f)

            for a in extract_file_annotations(o):
                if headers is None:
                    headers = list(a.keys())

                rows.append(list(a.values()))

    return headers, rows


def file_df():


    headers, rows = load_file_rows()

    return pd.DataFrame(rows, columns=headers)