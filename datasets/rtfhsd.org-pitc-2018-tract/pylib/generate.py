""" Example pylib functions"""

from geoid.tiger import Tract as TigerTract
from geoid.acs import AcsGeoid

def pitc(resource, doc, env, *args, **kwargs):
    """ An example row generator function.

    Reference this function in a Metatab file as the value of a Datafile:

            Datafile: python:pylib#row_generator

    The function must yield rows, with the first being headers, and subsequenct rows being data.

    :param resource: The Datafile term being processed
    :param doc: The Metatab document that contains the term being processed
    :param args: Positional arguments passed to the generator
    :param kwargs: Keyword arguments passed to the generator
    :return:


    The env argument is a dict with these environmental keys:

    * CACHE_DIR
    * RESOURCE_NAME
    * RESOLVED_URL
    * WORKING_DIR
    * METATAB_DOC
    * METATAB_WORKING_DIR
    * METATAB_PACKAGE

    It also contains key/value pairs for all of the properties of the resource.

    """

    from itertools import islice

    r = doc.reference('pitc_2018_source')
    
    yield "geoid tract community total_count".split()
    
    for d in  islice(r.iterdict,1,None):
        tract = d['Census Tract']
        try:
            a,b = tract.split('.')
        except ValueError:
            a,b = tract, ''
    
        geoid = TigerTract(6,73,(a.zfill(4)+b.zfill(2))).convert(AcsGeoid)
    
        yield (geoid, d['Census Tract'], d['Community'], d['Total Count'])
        
    
