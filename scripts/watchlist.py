"""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

watchlist:

Generates watchlist based on a selected satellite
"""
from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
from System import Random, Double
from System.Drawing import Color
import math
import sys
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox

# Getting the data table object
table_name = "WatchlistData"
data_table = Document.Data.Tables[table_name]

#Creating cursors to extract the data from the data table
columns = data_table.Columns
name_cursor = DataValueCursor.Create(columns["Well Name"])
status_cursor = DataValueCursor.Create(columns["Status Indicator"])
mrtll_cursor = DataValueCursor.Create(columns["Safely above MRTLL"])
constraint_cursor = DataValueCursor.Create(columns["Constraint"])
stability_cursor = DataValueCursor.Create(columns["Well Stability"])
period_cursor = DataValueCursor.Create(columns["Period"])
satellite_cursor = DataValueCursor.Create(columns["Satellite"])

well_names = set()
satellite = None
wells = []
# Get markings for current data table (Watchlist Data)
markings = Document.ActiveFilteringSelectionReference.GetSelection(data_table)
# Get each well for watchlist
for row in data_table.GetRows(markings.AsIndexSet(), satellite_cursor, name_cursor, status_cursor, mrtll_cursor, constraint_cursor, stability_cursor, period_cursor):
  if satellite == None:
    satellite = satellite_cursor.CurrentValue

  if name_cursor.CurrentValue not in well_names:
    well_names.add(name_cursor.CurrentValue) 
    wells.append({"name": name_cursor.CurrentValue, "status": status_cursor.CurrentValue, "mrtll": mrtll_cursor.CurrentValue, "constraint": constraint_cursor.CurrentValue, "stability": stability_cursor.CurrentValue, "period": period_cursor.CurrentValue})

# Generate watchlist
text_area = None
for visual in Document.ActivePageReference.Visuals:
  if "HtmlTextArea" in str(visual.TypeId):
    temp = visual.As[HtmlTextArea]()
    if temp.Title == "Watchlist":
      text_area = temp
      break

if text_area == None:
  text_area = Document.ActivePageReference.Visuals.AddNew[HtmlTextArea]()
  text_area.AutoConfigure()
  text_area.Title = "Watchlist"

headers = ["Well Name", "Status", "MRTLL", "Constraint", "Stability", "OFF Prediction"]

html_content = """
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
    font-size: 10pt;
}

.red {
  background-color: #C21807
}

.orange{
  background-color: #FEC34D
}

.green {
  background-color: #00CC00
}

.black{
  background-color: #000000;
  color: #FFFFFF;
}

</style>

"""

html_content = html_content + "<h2>" + satellite + "</h2> <table> <tr>" 

# Generate the header information
for header in headers:
  html_content = html_content + "<th>" + header + "</th>"
html_content = html_content + "</tr>"
# Update with data
for well in wells:
  html_content = html_content + "<tr>"
  # Well name
  html_content = html_content + "<td>" + well["name"] + "</td>"

  # Well status
  if well["status"] == "No Issue":
    html_content = html_content + '<td class="green">' + well["status"] + "</td>"
  elif well["status"] == "Warning":
    html_content = html_content + '<td class="orange">' + well["status"] + "</td>"
  elif well["status"] == "Action Needed":
    html_content = html_content + '<td class="red">' + well["status"] + "</td>"
  else:
    html_content = html_content + '<td class="black">' + well["status"] + "</td>"
  
  # MRTLL
  if well["mrtll"] == "Yes":
    html_content = html_content + '<td class="green">' + well["mrtll"] + "</td>"
  elif well["mrtll"] == "No":
    html_content = html_content + '<td class="red">' + well["mrtll"] + "</td>"
  else:
    html_content = html_content + '<td class="black">' + well["mrtll"] + "</td>"

  # Constraint
  if well["constraint"] == "Offline":
    html_content = html_content + '<td class="black">' + well["constraint"] + "</td>"
  else:
    html_content = html_content + "<td>" + well["constraint"] + "</td>"

  # Stability
  if well["stability"] == "Stable":
    html_content = html_content + '<td class="green">' + well["stability"] + "</td>"
  elif well["stability"] == "Close to Unstable":
    html_content = html_content + '<td class="orange">' + well["stability"] + "</td>"
  elif well["stability"] == "Unstable":
    html_content = html_content + '<td class="red">' + well["stability"] + "</td>"
  else:
    html_content = html_content + '<td class="black">' +  well["stability"] + "</td>"
  
  # Predicted offline period
  html_content = html_content + "<td>" + str(well["period"]) + "</td>"
  html_content = html_content + "</tr>"

html_content = html_content + "</table>"
text_area.HtmlContent = html_content
