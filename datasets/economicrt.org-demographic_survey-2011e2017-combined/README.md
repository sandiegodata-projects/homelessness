# LA County Homeless Survey

This dataset consists of records of in-person surveys of homeless individuals
in Los Angeles county, from 2011 to 2017, inclusive. The original data is
collected from annual surveys that are part of the annual Point In Time Count
of homeless individuqals conducted by the Los Angeles Homeless Services
Authority. The data is published by The Economic Roundtable.

The data in this package is significantly altered from the source file to make
analysis easier. Changes include:

* Added 'raceeth' field, which recodes the very many race/ethnicity values to a much simpler set that hamonizes with US Census categories.  
* Added 'sex' field, which recodes the 'gender' field.
* Broke out the type+year combination in 'survey_year' into two values. 

The Race/Ethnicity categories are: 

* hisp: Hispanic or Latino, of any race
* nhwhite: Non hispanic white
* black: Non hispanic  Black or African American
* aian: Non hispanic  American Indian / Alaskan Native
* asian: Non hispanic  Asian
* nhopi: Non hispanic Native Hawaiian / Other Pacific Islander
* other: Other race or multiple races

## Versions

1. Initial Version
2. Added schema descriptions
3. Broke out the survey_year into two fields, survey_type and year
4. Improved Metadata
