"""Read GCP annotations and create the GCP datasets"""
import json
import logging
from operator import itemgetter

import geopandas as gpd
import pandas as pd
from shapely import wkt

from . import gcp_list_url, intersections_url
from .download import download_to_file
from .images import *

logger = logging.getLogger('gcp')


def get_gcp_files():
    '''Yield all images, downloading if necessary'''

    with urllib.request.urlopen(gcp_list_url) as response:
        for l in response.readlines():
            url = l.strip().decode('ascii')

            yield download_to_file(url)


def extract_gcp_annotations(o):
    """Extract GCP data from VIA JSON file data"""

    cols = 'x y width height'.split()
    region_ig = itemgetter(*cols)

    d = o['_via_img_metadata']

    annotations = []

    for k, v in d.items():

        if k == 'example':
            continue

        for region in v['regions']:
            try:
                x, y, width, height = region_ig(region['shape_attributes'])

                annotations.append({
                    'image_url': v['filename'],
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'intersection': region['region_attributes']['Intersection']
                })

            except KeyError:
                logger.debug("Error. wrong keys in shape attributes: {}".format(region['shape_attributes']))


    return annotations


def load_gcp_rows():

    from dtcv.gcp import get_gcp_files, extract_gcp_annotations

    rows = []

    for e in get_gcp_files():
        with e.open() as f:
            rows.extend(extract_gcp_annotations(json.load(f)))

    return rows

def intersections_df():
    df  = pd.read_csv(intersections_url).rename(columns={'WKT':'geometry'})
    df['geometry'] = df.geometry.apply(wkt.loads)
    return gpd.GeoDataFrame(df, geometry='geometry')

def gcp_df():

    """Return a dataframe composed of records of GCP annotations downloaded from S3"""

    rows = load_gcp_rows()

    return pd.DataFrame([list(d.values()) for d in rows], columns=list(rows[0].keys()))

def gcp_transform_df():

    """Return a dataframe of GCP intersection polygons with Affine transformations to EPSG 2230"""

    intr_gpd = intersections_df()

    gcpdf = gcp_df()

    gcp_m = gcpdf.merge(intr_gpd, on='intersection').sort_values(['image_url', 'neighborhood', 'intersection'])
    df = gpd.GeoDataFrame(gcp_m)

    df['image_x'] = df.x + (df.width / 2)
    df['image_y'] = df.y + (df.height / 2)

    df['geo_x'] = df.geometry.x
    df['geo_y'] = df.geometry.y

    rows = []

    for name, g in df.groupby(['image_url', 'neighborhood']):
        g = g.sort_values(['image_y', 'image_x'])

        # Y Axis is inverted to match the Y axis orientation of the destination
        # geographic CRS. Adding 2000 to shift the values back to positive, so
        # the sorting algo in reorder_points will have the same sense of where the origin is
        image_p = Polygon([r.image_x, r.image_y] for idx, r in g.iterrows())
        image_p = invert_poly(Polygon(reorder_points(image_p)))

        geo_p = Polygon(reorder_points([[r.geo_x, r.geo_y] for idx, r in g.iterrows()]))

        rows.append([name[0], name[1], image_p.wkt, geo_p.wkt])

    #
    # Save the source ( image ) and dest (map ) polygons,
    # formed from the GCPs for each neighborhood
    #

    df = pd.DataFrame(rows, columns='url neighborhood source dest'.split())

    df['source'] = df.source.apply(wkt.loads)
    df['dest'] = df.dest.apply(wkt.loads)

    def _get_matrix(r):
        try:
            return json.dumps(get_matrix(r).tolist())
        except ValueError as e:
            print(r)
            print(e)

    df['matrix'] = df.apply(_get_matrix, axis=1)

    return df

