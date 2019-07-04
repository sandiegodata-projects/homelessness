
from geoid.tiger import Tract as TigerTract
from geoid.acs import AcsGeoid
from metapack import get_cache
from metapack.rowgenerator import PandasDataframeSource
    

def acs_tract(v):
    
    # Add the state and county code to make a Tiger Geoid, then
    # parse and convert
    return TigerTract(6,73,v).convert(AcsGeoid)
    
    
def generate_tracts(resource, doc, env, *args, **kwargs):



    pitc = doc.resource('pitc')\
        .geoframe()\
        .groupby(['Tract','Observe'])\
        .geometry.count().to_frame()\
        .unstack(-1)\
        .fillna(0)

    pitc.columns = ['handbuilt','individual','vehicle']
    pitc['total'] = pitc.sum(axis=1)

    yield from PandasDataframeSource('<df>',pitc , get_cache())