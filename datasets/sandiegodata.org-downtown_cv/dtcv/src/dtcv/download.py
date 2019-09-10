

from slugify import slugify
from pathlib import Path
import urllib.request
import shutil

import logging

logger = logging.getLogger('download')

def download_to_file(url):
    from tempfile import gettempdir

    slug = slugify(url)

    img_file = Path('/{}/{}'.format(gettempdir(), 'dtcv-' + slug))

    if not img_file.exists():
        with urllib.request.urlopen(url) as response, img_file.open('wb') as out_file:
            logger.debug('Downloaded {}'.format(url))
            shutil.copyfileobj(response, out_file)

    return img_file

