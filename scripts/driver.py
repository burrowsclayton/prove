"""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Driver:

This script runs the entire project. 

"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Scripting import ScriptDefinition
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox

# Getting the data table object
table_name = "Monthly Production information link"
data_table = Document.Data.Tables[table_name]

# Determines if a well has been selected by looking at the context
# of the filtering option "WELL_NAME"
well_selected = True
for filteringScheme in Document.FilteringSchemes:
  for filter in filteringScheme[data_table]:
    if filter.Name == "WELL_NAME":
      if str(filter.Context) == "WELL_NAME: ((All))":
        well_selected = False

if well_selected:
  # Produced the prove analysis scatter plot

  scatter_plot = clr.Reference[ScriptDefinition]()
  kmeans = clr.Reference[ScriptDefinition]()

  Document.ScriptManager.TryGetScript("scatter_plot", scatter_plot)
  Document.ScriptManager.TryGetScript("kmeans", kmeans)

  Document.ScriptManager.ExecuteScript(scatter_plot.ScriptCode, {})
  Document.ScriptManager.ExecuteScript(kmeans.ScriptCode, {})

else:
  # If no well has been selected then alert the user
  MessageBox.Show("Please select a well", "No well selected")
