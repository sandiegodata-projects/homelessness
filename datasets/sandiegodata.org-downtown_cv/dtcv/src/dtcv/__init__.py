"""

"""



image_list_url='http://ds.civicknowledge.org/downtownsandiego.org/homeless-count/urls.txt'

count_list_url='http://ds.civicknowledge.org/downtownsandiego.org/complete_annotations/count/urls.txt'

gcp_list_url='http://ds.civicknowledge.org/downtownsandiego.org/complete_annotations/gcp/urls.txt'

# Geo positions, in ESPG:2230 ( State plane 6, feet ) for intersections.
intersections_url = 'http://ds.civicknowledge.org.s3.amazonaws.com/downtownsandiego.org/annotations/gcp_intersections_2230.csv'


from .gcp import gcp_transform_df, gcp_df, intersections_df
from .counts import file_df, count_df

from .images import get_image