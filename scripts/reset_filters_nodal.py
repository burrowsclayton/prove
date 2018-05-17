""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Reset Filters:

This script resets the WELL_NAME and FIELD_NAME filters

"""
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Filters import *

# Getting the data table object
table_name = "NodalData"
data_table = Document.Data.Tables[table_name]

# Resets all filters in list
filters_to_reset = ["WELL_NAME","SATELLITE","Date"]

# loop through every filter in document and reset if in the filter_to_reset list
for filtering_scheme in Document.FilteringSchemes:
  for filter in filtering_scheme[data_table]:
    if filter.Name in filters_to_reset:
      filter.Reset()
