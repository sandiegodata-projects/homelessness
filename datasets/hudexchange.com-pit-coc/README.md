# HUD Point in Time Counts by CoC

HUD publishes an Excel workbook with sheltered and unsheltered counts,
aggregated to CoC, for the whole country, for 2007 on. In this dataset, each
year is in a seperate worksheet, and later years have more columns than earlier
years, and most column names include the year as a suffix. 

This data package combines al of these years into a single file, with
normalized column names. Cells in years that don't have a column that are in
later years are filled with nulls, and each row is prefixed with the year of
the file that the original row was sourced from.

For a graphic view of which columns are missing, by year ( actually by position
in the dataset ) see the null map at the end of the [EDA
notebook](https://github.com/sandiegodata-projects/homelessness/blob/master/datasets/hudexchange.com-pit-coc/notebooks/eda-pitc_coc.ipynb ).

## Revisions to the Historic Point-in-Time Estimates

The data source file includes this note:


On rare occasions, the Point-in-Time estimates published in prior editions of the AHAR have been subsequently updated. The estimates described in this file represent the latest versions of these data (as of the publication of this file). The revisions are summarized below:

1. Beginning in the 2014 AHAR Part 1, the PIT estimates of unsheltered people experiencing homelessness in the Los Angeles City and County CoC, CA-600, were updated for the years 2007–2013. Within the CoC, the adjustments subtracted: 20,746 total people from 2007 and 2008; 9,451 total people in 2009 and 2010; 10,800 total people in 2011 and 2012; and 18,274 total people from 2013. These adjustments also caused drops in the key unsheltered populations reported on the AHAR, individuals, people in families, veterans, and chronically homeless individuals. More details on the size of each adjustment, by population, can be found in the 2014 AHAR Part 1.

2. Beginning in the 2014 AHAR Part 1, the PIT estimate of veterans experiencing homelessness in shelter projects in the Phoenix/Mesa/Maricopa County Regional CoC, AZ-502, was updated for the year 2013, increasing by 214 veterans. This update did not change the total number of people experiencing homelessness in shelter projects (or overall) in the CoC—just the number of those people who were classified as veterans.

3. Beginning in the 2015 AHAR Part 1, the PIT estimates of unsheltered people experiencing homelessness in the Las Vegas/Clark County CoC, NV-500, were updated for the years 2007–2014. Within the CoC, the adjustments subtracted: 3,884 total people from 2007 and 2008; 3,389 total people in 2009 and 2010; 1,429 total people in 2011 and 2012; 1,404 total people from 2013; and 1,974 total people from 2014. These adjustments also caused drops in the key unsheltered populations reported on the AHAR, individuals, people in families, veterans, and chronically homeless individuals. More details on the size of each adjustment, by population, can be found in the 2015 AHAR Part 1.

4. Beginning in the 2015 AHAR Part 1, the PIT estimates of veterans experiencing homelessness in the Anchorage CoC, AK-500, were updated for the year 2014. The sheltered estimate for this CoC increased by 71 veterans, and the unsheltered estimate increased by 18 veterans. Neither of these updates changed the total number of people experiencing homelessness in the CoC—just the number of those people who were classified as veterans.

5. Beginning in the 2017 AHAR Part 2 and the 2018 AHAR Part 1, the PIT estimates of unsheltered people experiencing homelessness in the Los Angeles City and County CoC, CA-600, were updated for the year 2017, decreasing by a total of 2,746 people. The adjustment also caused drops in the key unsheltered populations reported on the AHAR, individuals, people in families, veterans, and chronically homeless individuals. More details on the size of each adjustment, by population, can be found in the 2017 AHAR Part 2 and the 2018 AHAR Part 1.
