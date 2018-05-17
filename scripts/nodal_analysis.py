""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Scatter Plot:

Creates the scatter plot
"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Returns the page with the name give
def get_plot_page(name_of_page="Nodal Plots"):
  for page in Document.Pages:
    if page.Title == name_of_page:
      return page
  page = Document.Pages.AddNew()
  page.AutoConfigure()
  page.Title = "Nodal Plots"
  return page
# Getting the data table object
data_table = Document.Data.Tables["NodalData"]

# Getting the well name filter
name_filter = None
date_filter = None
for filtering_scheme in Document.FilteringSchemes:
  # Select the filter that is named WELL_NAME
  for filter in filtering_scheme[data_table]:
    # There may be multiple filters with this name, we want the filter
    # that comes from the box filter which is selected by the user. 
    if str(filter.TypeId) == "TypeIdentifier:Spotfire.ListBoxFilter" and filter.Name == "WELL_NAME" and name_filter == None:
      name_filter = filter
    if str(filter.TypeId) == "TypeIdentifier:Spotfire.ListBoxFilter" and filter.Name == "Date" and date_filter == None:
      date_filter = filter

# Extracting the name of each well that has been selected
# The filtering context looks like:
# WELL_NAME: (Wackett 8, Wackett 9, Wackett 10)

# Get the two indexs of the paraenthesis
values_begin = str(name_filter.Context).find('(') + 1
values_end = str(name_filter.Context).find(')')
# Remove the characters before and after the paranthesis including 
# the parathensis, the string will then become
# "Wackett 9, Wackett 8, Wackett 10" then split on commas
names = str(name_filter.Context)[values_begin:values_end].split(',')

# Do the same for the date
# We will only accept one date
values_begin = str(date_filter.Context).find('(') + 1
values_end = str(date_filter.Context).find(')')
date =  str(date_filter.Context)[values_begin:values_end]

plots_page = get_plot_page("Nodal Plots")

for well_name in names:
  # Must set the name to uppercase since this is how the names are stored in the tavle
  well_name = well_name.upper()
  # All names besides the first will have a leading white space, need
  # to remove the leading white space
  well_name = well_name[1:] if well_name[0] == " " else well_name
  # Creating the scatter plots
  scatter_plot = plots_page.Visuals.AddNew[ScatterPlot]()
  # Linking the data table with the newly created scatter plot
  scatter_plot.Data.DataTableReference = data_table
  # Auto configures the scattter plot settings, needed for markings
  scatter_plot.Data.AutoConfigure()
  # Setting the x and y axis of the scatter plot, and setting them to use a log scale
  scatter_plot.YAxis.Expression = "[IPR (kPag)],[VLP (kPag)],[Operating Point (kPag)]"
  scatter_plot.XAxis.Expression = "[Gas Rate (e3m3/day)]"
  

  # Setting the filtering options
  scatter_plot.Data.UseActiveFiltering = False
  scatter_plot.Data.WhereClauseExpression = '[WELL_NAME] ~= "^' + well_name + '$" and [Date] ~= "^' + date + '$"'

  # Display settings of the scatter plot
  scatter_plot.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)
  scatter_plot.Title = well_name
  scatter_plot.ColorAxis.Expression = "<[Axis.Default.Names]>"

Document.ActivePageReference = plots_page
