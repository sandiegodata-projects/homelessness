# Homelessness Demographic Surveys

The Los Angeles Homeless Services Authority (LAHSA) conducts annual in-person
surveys of the unsheltered homeless population in Los Angeles. This data
package includes the standardized versions of the annual survey data for 2011
through 2017, combined into a single file (``combined_survey``) and another
multi year file that was produced by UCLA, which includes only the common
columns from the multi-year files. (``multiyear_survey``)

The ``combined_survey`` includes all of the columns from all of the years,
although many columns only exist for one year. The result is that many of
variables are null for one or more of the survey years.

The source for the ``multiyear_survey`` file was produced by UCLA and includes
only a subset of the columns available in ``combined_survey``, but the
variables have many more non-null values.

The best way to compare these files is to look at the EDA notebooks for the
files, and in particular, the Null map at the end of the notebook.

## Processing

Both files have some additional processing

- 'NA' values are converted to blank cells
- A new ``sex`` column which codes the genders Male as 'M', Female as 'F', and all others as 'U'
- A new ``raceeth`` variable for census race and ethnicity categories with values for ``black``, ``white``, ``asian``, ``aian``, ``aian``, ``nhopi``, ``hisp`` and ``other``, based on keywords in the ``Race_Full`` variable. 
- Strip trailing spaces from `Race_Full`
- A new ``geoid`` variable that holds the census tract variable converted to a format Census geoid. 
- A new ``year`` variable that holds an integer version of the `Survey_Year`` variable
