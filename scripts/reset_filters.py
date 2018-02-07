""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Reset Filters:

This script resets the WELL_NAME and FIELD_NAME filters

"""
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Filters import *

data_table = Document.Data.Tables
data_table_name = [table.Name for table in data_table][0]
data_table = data_table[ data_table_name ]

filters_to_reset = ["WELL_NAME","FIELD_NAME"]

for filtering_scheme in Document.FilteringSchemes:
  for filter in filtering_scheme[data_table]:
    if filter.Name in filters_to_reset:
      filter.Reset()