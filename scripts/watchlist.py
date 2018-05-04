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

def htmlName(well):
  return "<td>" + well["name"] + "</td>"
  
def htmlStatus(well):
  if well["status"] == "No Issue":
    return '<td class="green">' + well["status"] + "</td>"
  elif well["status"] == "Warning":
   return '<td class="orange">' + well["status"] + "</td>"
  elif well["status"] == "Action Needed":
    return '<td class="red">' + well["status"] + "</td>"
  
  return '<td class="black">' + well["status"] + "</td>"
    
def htmlMrtll(well):
  if well["mrtll"] == "Yes":
    return '<td class="green">' + well["mrtll"] + "</td>"
  elif well["mrtll"] == "No":
    return '<td class="red">' + well["mrtll"] + "</td>"
  
  return '<td class="black">' + well["mrtll"] + "</td>"

def htmlConstraint(well):
  if well["constraint"] == "Offline":
    return '<td class="black">' + well["constraint"] + "</td>"
  
  return "<td>" + well["constraint"] + "</td>"
    
def htmlStability(well):
  if well["stability"] == "Stable":
    return '<td class="green">' + well["stability"] + "</td>"
  elif well["stability"] == "Close to Unstable":
    return '<td class="orange">' + well["stability"] + "</td>"
  elif well["stability"] == "Unstable":
    return '<td class="red">' + well["stability"] + "</td>"
    
  return '<td class="black">' +  well["stability"] + "</td>"
    
def htmlPeriod(well):
  if well['offline'] == 'Offline':
    return '<td class="black"> Offline </td>'
      
  return "<td>" + well["offline"] + "</td>"

def rankStatus(current, prev):
  if (prev['status'] == 'No Issue') and (current['status'] == 'Warning'):
    current['rank'] += 1 / current['period']
  elif (prev['status'] == 'No Issue') and (current['status'] == 'Action Needed'):
    current['rank'] += 2 / current['period']
  elif (prev['status'] == 'No Issue') and (current['status'] == 'Offline'):
    current['rank'] += 3 / current['period']
    current['offline'] = str(current['period']*3) + " Months"
  elif (prev['status'] == 'Warning') and (current['status'] == 'Action Needed'):
    current['rank'] += 2 / current['period']
  elif (prev['status'] == 'Warning') and (current['status'] == 'Offline'):
    current['rank'] += 3 / current['period']
    current['offline'] = str(current['period']*3) + " Months"
  elif (prev['status'] == 'Action Needed') and (current['status'] == 'Offline'):
    current['rank'] += 3 / current['period']
    current['offline'] = str(current['period']*3) + " Months"
  return current

    
def rankMrtll(current, prev):
  if (prev['mrtll'] == 'Yes') and (current['mrtll'] == 'No'):
    current['rank'] += 2 / current['period']
  elif (prev['mrtll'] == 'Yes') and (current['mrtll'] == 'Offline'):
    current['rank'] += 3 / current['period']
  elif (prev['mrtll'] == 'No') and (current['mrtll'] == 'Offline'):
    current['rank'] += 3 / current['period']
  return current
  
def rankStability(current, prev):
  if (prev['stability'] == 'Stable') and (current['stability'] == 'Close to Unstable'):
    current['rank'] += 1 / current['period']
  elif (prev['stability'] == 'Stable') and (current['stability'] == 'Unstable'):
    current['rank'] += 2 / current['period']
  elif (prev['stability'] == 'Stable') and (current['stability'] == 'Offline'):
    current['rank'] += 3 / current['period']
  elif (prev['stability'] == 'Close to Unstable') and (current['stability'] == 'Unstable'):
    current['rank'] += 2 / current['period']
  elif (prev['stability'] == 'Close to Unstable') and (current['stability'] == 'Offline'):
    current['rank'] += 3 / current['period']
  elif (prev['stability'] == 'Unstable') and (current['stability'] == 'Offline'):
    current['rank'] += 3 / current['period']
  return current
  
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

satellite = None
rankedWells = []
allRows = []
# Get markings for current data table (Watchlist Data)
markings = Document.ActiveFilteringSelectionReference.GetSelection(data_table)
# Get each well for watchlist
for row in data_table.GetRows(markings.AsIndexSet(), satellite_cursor, name_cursor, status_cursor, mrtll_cursor, constraint_cursor, stability_cursor, period_cursor):
  if satellite == None:
    satellite = satellite_cursor.CurrentValue

  allRows.append({"name": name_cursor.CurrentValue, "status": status_cursor.CurrentValue, "mrtll": mrtll_cursor.CurrentValue, "constraint": constraint_cursor.CurrentValue, "stability": stability_cursor.CurrentValue, "period": period_cursor.CurrentValue})

# Perform the ranking
well_names = set()
wells = []
# Loop through each well
for well in allRows:
  if well["name"] not in well_names:
    well_names.add(well["name"])
    rankedWell = dict(well)
    rankedWell['rank'] = 0
    rankedWell['offline'] = 'N/A'

    # Get all wells with the same name as the current well to get all periods
    # This can be made shorter in terms of execution time if you enumerate 
    # and search from i or whatever, but if you think about it you can
    periods = []
    for w in allRows:
      if w["name"] == rankedWell["name"]:
        periods.append(w)
      if len(periods) >= 5:
        break
    
    prev_period = None
    for period in periods:
      # If it is offline in its initial period then it is given a rank of 0
      # and period is set to zero
      if prev_period == None:
        if period["status"] == "Offline":
          rankedWell['offline'] = 'Offline'
          break
      else:
        period['rank'] = rankedWell['rank']
        period['offline'] = rankedWell['offline']
        rankedWell = rankStatus(period, prev_period)
        rankedWell = rankMrtll(period, prev_period)
        rankedWell = rankStability(period, prev_period)

      prev_period = dict(period)
    
    # Restore the current conditions for watchlist printing
    for key in periods[0].keys():
      rankedWell[key] = periods[0][key]
    wells.append(rankedWell)
    

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
    border: 3px solid #dddddd;
    text-align: center;
    padding: 8px;
    font-size: 12pt;
    font-weight: bold;
}

.red {
  background-color: #e11807;
  color: #FFFFFF
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

.gray{
  background-color: gray;
}

</style>

"""

html_content += "<h2>" + satellite + "</h2> <table> <tr>" 

# Generate the header information
for header in headers:
  html_content += '<th class="gray">' + header + "</th>"
html_content += "</tr>"


# Sort wells based on ranked, higher the rank the more important
wells = sorted(wells, key=lambda k: k['rank'], reverse=True)
for well in wells:
  html_content += "<tr>"
  html_content += htmlName(well)
  html_content += htmlStatus(well)
  html_content += htmlMrtll(well)
  html_content += htmlConstraint(well)
  html_content += htmlStability(well)
  html_content += htmlPeriod(well)
  html_content +=  "</tr>"

html_content += "</table>"
text_area.HtmlContent = html_content
