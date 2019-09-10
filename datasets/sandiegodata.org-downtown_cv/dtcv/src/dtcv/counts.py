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


def extract_count_region(o):
    pass

    reg_cols = 'Type count'.split()
    reg_ig = itemgetter(*reg_cols)

    shape_cols = 'cx cy r'.split()
    shape_ig = itemgetter(*shape_cols)
    rows = []

    d = o['_via_img_metadata']

    for k, v in d.items():
        if k == 'example':
            continue

        for region in v['regions']:
            try:

                cx, cy, r = list(shape_ig(region['shape_attributes']))
                typ, count = list(reg_ig(region['region_attributes']))

                rows.append({
                    'image_url' : v['filename'],
                    'cx': cx,
                    'cy': cy,
                    'r': r,
                    'type': typ,
                    'count': count

                })
            except KeyError as e:
                logger.error("Error. wrong keys in shape attributes: ", region['shape_attributes'])

def extract_count_file_annotations(o):

    rows = []

    file_cols = 'date neighborhood total_count temp rain '.split()

    def get_file_cols(d):
        row = {}
        for c in file_cols:
            row[c] = d.get(c)

        return row

    d = o['_via_img_metadata']

    for k, v in d.items():
        if k == 'example':
            continue

        image_url = v['filename']

        try:
            row = {'image_url': image_url}
            row.update( get_file_cols(v['file_attributes']))

            rows.apprnd(row)

        except KeyError as e:
            logger.error("Error in extracting file annotations. ", e, v['file_attributes'])

    return rows


def extract_count_annotations(o):
    """Extract GCP data from VIA JSON file data"""



    df = pd.DataFrame(rows, columns=['filename', 'url'] + shape_cols + reg_cols).merge(file_df, on='url')

    df = df.drop(columns=['filename_x', 'neighborhood_x']) \
        .rename(columns={'filename_y': 'filename', 'neighborhood_y': 'neighborhood'})

    df['count'] = df['count'].replace('', 1)

    return df