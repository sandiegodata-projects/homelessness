""" Example pylib functions"""


def row_generator(resource, doc, env, *args, **kwargs):
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

    yield 'a b c'.split()

    for i in range(10):
        yield [i, i*2, i*3]


def parse_tract(v, row, row_n, i_s, i_d, header_s, header_d,scratch, errors, accumulator):
    """ Parse the tract number, within Los Angeles County
    """

    from geoid.acs import Tract
    
    # 6 == CA, 037 == Los Angeles County
    return Tract(6,37,v)