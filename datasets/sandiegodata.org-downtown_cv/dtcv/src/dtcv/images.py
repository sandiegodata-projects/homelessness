"""Image manipulations, for images using the OpenCV image format ( numpy arrays)"""


from . import image_list_url
from .download import download_to_file
import numpy as np
from shapely.geometry import Polygon
from shapely import wkt
from pathlib import Path
import urllib.request
import cv2

# Pad and unpack the transformation matrix to be 3x1 or 3x3,
# necessary for it to handle both rotation and translation
pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
unpad = lambda x: x[:, :-1]

def norm(pri):
    '''Normalize a matrix to 0->1'''
    pri = pri.copy()
    pri[:, 0] = pri[:, 0] - pri[:, 0].mean()
    pri[:, 0] = pri[:, 0] / pri[:, 0].max()
    pri[:, 1] = pri[:, 1] - pri[:, 1].mean()
    pri[:, 1] = pri[:, 1] / pri[:, 1].max()
    return pri

def get_image(url, return_file_path=False):
    '''Download an image and cache the file inthe tmp directory. '''

    img_file = download_to_file(url)

    with img_file.open('rb') as f:
        img_array = np.array(bytearray(f.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        if return_file_path:
            return img, img_file
        else:
            return img

def get_images():
    '''Yield all images, downloading if necessary'''

    with urllib.request.urlopen(image_list_url) as response:
        for l in response.readlines():
            url = l.strip().decode('ascii')
            p = Path(url)
            parts = url.split('/')
            year, month = int(p.stem[:4]), int(p.stem[4:6])
            neighborhood = parts[-2]

            img, img_file = get_image(url, True)

            yield img, img_file, year, month, neighborhood


def poly_to_array(poly):

    try:
        return  np.array(poly.exterior.coords)[:-1]
    except AttributeError:
        return poly


def upper_left(poly):
    """Find the point closest to the origin, in image coordinates"""

    try:
        poly.encode()
        pts = poly_to_array(wkt.loads(poly))
    except AttributeError:
        pts = poly_to_array(poly)

    dists = [np.linalg.norm(np.array((0, 0)) - p) for p in pts]

    return pts[np.argmin(dists)]

def reorder_points(v):
    """Reorder points to ensure the shape is valid. The only works if all of the points
    are on the convex hull, which is true for our shapes. """

    from math import sqrt

    try:
        points = poly_to_array(v).tolist()
    except AttributeError:
        points = v # Hopefully already a list.

    points = poly_to_array(Polygon(v).convex_hull).tolist()

    # Find the point closest to the origin
    # Norming ensures origin finding is consistent. I guess.
    normed_points = norm(np.array(points)) + 10  # +10 to void div by zero in distance

    mp = next(iter(sorted(normed_points, key=lambda p: sqrt(p[0] ** 2 + p[1] ** 1))))

    # Rotate the list of points so the mp point is first in the list
    mpos = normed_points.tolist().index(mp.tolist())
    points = points[mpos:] + points[:mpos]

    return np.array(points)


def solve_transform(primary, secondary):

    primary = reorder_points(poly_to_array(primary))
    secondary = reorder_points(poly_to_array(secondary))

    A, res, rank, s = np.linalg.lstsq(pad(primary), pad(secondary), rcond=None)

    A[np.abs(A) < 1e-12] = 0  # Get rid of really small values.

    return A, primary, secondary

def invert_point(p):
    x,y = p

    y = -y + 2000
    return (x,y)

def invert_poly(poly):

    return Polygon( invert_point(p) for p in poly_to_array(poly))

def transform_point(A, x):
    # The extra np.array in pad() presumes this is a point, not a matrix
    # The final [0] unpacks back to a point.

    return unpad(np.dot(pad(np.array([x])), A))[0]

def transform_points(A, x):
    return unpad(np.dot(pad(x), A))

def get_transform(r):
    A, transform = solve_transform(r.source, r.dest)
    return transform


def get_matrix(r):
    A, pri, sec = solve_transform(r.source, r.dest)
    return A


