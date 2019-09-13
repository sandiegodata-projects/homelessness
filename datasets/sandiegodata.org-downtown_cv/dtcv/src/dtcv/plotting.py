import dtcv
import matplotlib.pyplot as plt
import numpy as np
from shapely import wkt
def grid_shape(i, max_x=4):
    """Return a good grid shape, in x,y, for a number if items i"""

    from math import sqrt, ceil
    x = round(sqrt(i))

    if x > max_x:
        x = max_x

    y = ceil(i / x)

    return x, y


def plot_image_and_poly(r, shape=None, figsize=(20, 20), max_x=4, titlef=None):
    """Given a row in the intersection_regions dataframe, plot the image and
    the intersection polygon"""


    try:
        records = [e[1] for e in r.iterrows()]
        ncols, nrows = grid_shape(len(r), max_x=max_x)
    except AttributeError:
        records = [r]
        ncols, nrows = 1, 1

    if shape is not None:
        ncols, nrows = shape

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    try:
        axes = axes.flat
    except AttributeError:
        axes = [axes]

    for ax, rec in zip(axes, records):
        img = dtcv.get_image(rec.image_url)
        ax.imshow(img)
        pts = np.array((wkt.loads(rec.source)).exterior.coords)
        ax.plot([e[0] for e in pts], [e[1] for e in pts], marker='s', color='red')
        if titlef:
            ax.set_title(titlef(rec))



# Generate random colormap
# From https://raw.githubusercontent.com/delestro/rand_cmap/master/rand_cmap.py
def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np



    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    elif type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    return random_colormap

def show_colormap(cmap):
    from matplotlib import colors, colorbar
    from matplotlib import pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

    nlabels = cmap.N

    bounds = np.linspace(0, nlabels, nlabels + 1)
    norm = colors.BoundaryNorm(bounds, nlabels)

    cb = colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, spacing='proportional', ticks=None,
                               boundaries=bounds, format='%1i', orientation=u'horizontal')


def resample_reorder_cmap(cmap, N, seed=1337):
    '''Downsamples a colormap, then reorder the colors randomly

    >>> resample_reorder_cmap(plt.get_cmap('plasma'),5)

    '''
    from matplotlib.colors import LinearSegmentedColormap
    import random
    rcmap = cmap._resample(N)

    l = [rcmap(i) for i in range(N)] #  Extract all of the values
    random.seed(seed)  # Always get the same ordering.
    random.shuffle(l)

    return LinearSegmentedColormap.from_list('rand_' + cmap.name, l, N=N)
