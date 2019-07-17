# San Diego Point In Time Count 2018, Tracts


This dataset includes the sheltered and unsheltered homeless counts from the San Diego Continuum of Care, CA-601. 

## Caveats

The sheltered count, ``sheltered_2018``, is based on a data extract from HUD,
and is similar, although not exactly, the same as the 2018 records for CA-601
from the official HUD HIC dataset, which [has been packaged to combine multiple
years. ](https://data.sandiegodata.org/dataset/hudexchange-info-hic-project/).
The ``sheltered_2018`` resource in this dataset differs from the HUD dataset in
two rows ( 336790, 347741 ) which appear to have been removed in an update made
after source file for ``sheltered_2018`` was extracted. However, the PITC beds
for the removed rows appear to have been re-allocated, because both datasets
have the same value for the sum of the ``pit_count`` variable. For many
analytical uses, these datasets will be identical.

However, the [HUD HIC
file]((https://data.sandiegodata.org/dataset/hudexchange-info-hic-project/))
has many columns that the ``sheltered_2018`` file does not, including street
addresses for the facilities

## Versions

1. Initial Version
2. Added descriptions to data dictionary

