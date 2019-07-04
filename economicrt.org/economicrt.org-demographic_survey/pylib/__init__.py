""" Example pylib functions"""


def combine(resource, doc, env, *args, **kwargs):
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

    import petl as etl
    import pandas as pd
    from metapack_build.rowgenerator import copy_reference_group

    # NOTE! Internally, this function required the "Group" and "RefArgs" properties of the resource. 

    data = list(copy_reference_group(resource,doc, env, *args, **kwargs))

    df = pd.DataFrame(data[1:], columns = data[0])

    df['sex'] = df.gender.replace({
        'Male': 'M',
        'Female': 'F',
        'Unknown': 'U',
        'Transgender': 'U'
    })

    df['race_full'] = df.race_full.str.strip()

    s = df.race_full.astype(str).apply

    df['black'] = s( lambda v: 1 if 'black' in v.lower() or 'african' in v.lower() else 0)
    df['white'] = s( lambda v: 1 if 'european' in v.lower() or 'white' in v.lower() or 'causian' in v.lower() else 0)
    df['asian'] = s( lambda v: 1 if 'asian' in v.lower() else 0)
    df['aian'] =  s( lambda v: 1 if 'indian' in v.lower()  or 'alaska' in v.lower() else 0)
    df['nhopi'] =  s( lambda v: 1 if 'hawaii' in v.lower()  or 'pacific' in v.lower() else 0)
    df['hisp'] =  s( lambda v: 1 if 'hisp' in v.lower()  or 'latin' in v.lower() else 0)
    df['other'] = (df.black + df.white + df.asian + df.aian + df.hisp + df.nhopi ) 

    def raceeth(r):
    
        if r.hisp or r.ethnicity == 'Latino':
            return 'hisp'
        elif r.other > 1:
            return 'other'
        elif r.black:
            return 'black'
        elif r.aian:
            return 'aian'
        elif r.nhopi:
            return 'nhopi'
        elif r.asian:
            return 'asian'
        elif r.white:
            return 'nhwhite'
        else:
            return 'other'

    df['raceeth'] = df.apply(raceeth, axis=1)
    df.drop(columns='black white asian aian nhopi hisp other'.split(), inplace = True)

    # Re-order the columns
    cut_out = ['col0','x','x1','x1_1','x1_2', 'weights']

    left_cols = ['year','gender', 'sex', 'raceeth', 'race_full','race_recode', 'ethnicity',
                 'age','birth_year', 'census_tract', 'census_tract_or_shelterid', 'spa']

    all_cols = left_cols + list(sorted(set(df.columns) - set(left_cols) - set(cut_out))) + ['weights']

    return df[all_cols]



