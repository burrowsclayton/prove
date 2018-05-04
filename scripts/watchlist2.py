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
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MessageBox

# Functions:
# Because of Spotfires limited environment I have to define everything in one 
# location so I will define all functions at the beginning of a document

# Generates the HTML content for a column of the given well
def htmlName(well):
  return '<td>' + well['name'] + '</td>'
  
def htmlStatus(well):
  if well['status'] == 'No Issue':
    return '<td class="green">' + well['status'] + '</td>'
  elif well['status'] == 'Warning':
   return '<td class="orange">' + well['status'] + '</td>'
  elif well['status'] == 'Action Needed':
    return '<td class="red">' + well['status'] + '</td>'
  else:
    return '<td class="black">' + well['status'] + '</td>'
    
def htmlMrtll(well):
  if well['mrtll'] == 'Yes':
    return '<td class="green">' + well['mrtll'] + '</td>'
  elif well['mrtll'] == 'No':
    return '<td class="red">' + well['mrtll'] + '</td>'
  else:
    return '<td class="black">' + well['mrtll'] + '</td>'

def htmlConstraint(well):
  if well['constraint'] == 'Offline':
    return '<td class="black">' + well['constraint'] + '</td>'
  else:
    return '<td>' + well['constraint'] + '</td>'
    
def htmlStability(well):
  if well['stability'] == 'Stable':
    return '<td class="green">' + well['stability'] + '</td>'
  elif well['stability'] == 'Close to Unstable':
    return '<td class="orange">' + well['stability'] + '</td>'
  elif well['stability'] == 'Unstable':
    return '<td class="red">' + well['stability'] + '</td>'
  else:
    return '<td class="black">' +  well['stability'] + '</td>'
    
def htmlPeriod(well):
  if well['offline'] == 'Offline':
    return '<td class="black"> Offline </td>'
  else:
    return '<td>' + well['offline'] + '</td>'


# Updates the rank of a well based on the current and previous periods
# Looks at the change in Status Indicator
def rankStatus(well, current, prev):
  if (prev['status'] == 'No Issue') and (current['status'] == 'Warning'):
    well['rank'] += 1 / current['period']
  elif (prev['status'] == 'No Issue') and (current['status'] == 'Action Needed'):
    well['rank'] += 2 / current['period']
  elif (prev['status'] == 'No Issue') and (current['status'] == 'Offline'):
    well['rank'] += 3 / current['period']
    well['offline'] = str(current['period']*3) + " Months"
  elif (prev['status'] == 'Warning') and (current['status'] == 'Action Needed'):
    well['rank'] += 2 / current['period']
  elif (prev['status'] == 'Warning') and (current['status'] == 'Offline'):
    well['rank'] += 3 / current['period']
    well['offline'] = str(current['period']*3) + " Months"
  elif (prev['status'] == 'Action Needed') and (current['status'] == 'Offline'):
    well['rank'] += 3 / current['period']
    well['offline'] = str(current['period']*3) + " Months"

# Updates the ranke of a well based on the current and previous periods
# Looks at the change in MRTLL
def rankMrtll(well, current, prev):
  if (prev['mrtll'] == 'Yes') and (current['mrtll'] == 'No'):
    well['rank'] += 2 / current['period']
  elif (prev['mrtll'] == 'Yes') and (current['mrtll'] == 'Offline'):
    well['rank'] += 3 / current['period']
  elif (prev['mrtll'] == 'No') and (current['mrtll'] == 'Offline'):
    well['rank'] += 3 / current['period']

# Updates the ranke of a well based on the current and previous periods
# Looks at the change in Stability
def rankStability(well, current, prev):
  if (prev['stability'] == 'Stable') and (current['stability'] == 'Close to Unstable'):
    well['rank'] += 1 / current['period']
  elif (prev['stability'] == 'Stable') and (current['stability'] == 'Unstable'):
    well['rank'] += 2 / current['period']
  elif (prev['stability'] == 'Stable') and (current['stability'] == 'Offline'):
    well['rank'] += 3 / current['period']
  elif (prev['stability'] == 'Close to Unstable') and (current['stability'] == 'Unstable'):
    well['rank'] += 2 / current['period']
  elif (prev['stability'] == 'Close to Unstable') and (current['stability'] == 'Offline'):
    well['rank'] += 3 / current['period']
  elif (prev['stability'] == 'Unstable') and (current['stability'] == 'Offline'):
    well['rank'] += 3 / current['period']

watchlist_dt = Document.Data.Tables['WatchlistData']

#Creating cursors to extract the data from the data table
columns = watchlist_dt.Columns
satellite_cursor = DataValueCursor.Create(columns['Satellite'])
name_cursor = DataValueCursor.Create(columns['Well Name'])
status_cursor = DataValueCursor.Create(columns['Status Indicator'])
mrtll_cursor = DataValueCursor.Create(columns['Safely above MRTLL'])
constraint_cursor = DataValueCursor.Create(columns['Constraint'])
stability_cursor = DataValueCursor.Create(columns['Well Stability'])
period_cursor = DataValueCursor.Create(columns['Period'])

satellite = None # Used to set title of watchlist
rows = [] # contains a list of rows that represents the data table
wells = [] # contains the wells that will be displayed on the watch list
# Gets the rows that match the filtering scheme
selected_rows = Document.ActiveFilteringSelectionReference.GetSelection(watchlist_dt) 

# Extract each row and save it to rows
for _ in watchlist_dt.GetRows(selected_rows.AsIndexSet(), satellite_cursor, 
                              name_cursor, status_cursor, mrtll_cursor, \
                              constraint_cursor, stability_cursor, \
                              period_cursor):
  if satellite == None:
    satellite = satellite_cursor.CurrentValue

  row = {
    'name': name_cursor.CurrentValue, \
    'status': status_cursor.CurrentValue, \
    'mrtll': mrtll_cursor.CurrentValue, \
    'constraint': constraint_cursor.CurrentValue, \
    'stability': stability_cursor.CurrentValue, \
    'period': period_cursor.CurrentValue, \
    'rank': 0, \
    'offline': 'N/A'
  }

  rows.append(row)

# Used to keep track of wells that have been saved, this is because there are 
# multiple rows  for one well just at different periods, we do not want to rank
# a well multiple times. 
well_names = set()
for i, row in enumerate(rows):
  # Check to see if well name has been saved
  if row['name'] not in well_names:
    well_names.add(row['name'])
    well = dict(row) # Copy current row to create ranked well
    well_periods = [] # Contains dictionaries of periods for a well
    # Can only be a maximum of 5 dates so only loop for this amount
    for j in range(i, i + 5):
      r = rows[j]
      # If they have the same name then the rows are for the same well
      # but different period so add to our period data
      if r['name'] == well['name']:
        well_periods.append(r)

    prev_period = None # Keeps track of row for previous period for ranking
    for current_period in well_periods:
      # If it is offline in its initial period then it is given a rank 
      # of zero and offline is set to offline
      if prev_period == None:
        if current_period['status'] == 'Offline':
          well['offline'] = 'Offline'
          well['rank'] = -1
          break
      else:
        rankStatus(well, current_period, prev_period)
        rankMrtll(well, current_period, prev_period)
        rankStability(well, current_period, prev_period)
      prev_period = current_period
    
    # Add well to wells now that is has been given a rank
    wells.append(well)

# Generate HTML watchlist
watchlist = None
# Must loop through each visual to find the text area named Watchlist
for v in Document.ActivePageReference.Visuals:
  if 'HtmlTextArea' in str(v.TypeId):
    if v.Title == 'Watchlist':
      watchlist = v.As[HtmlTextArea]()

# If it does not exists we must create a new text area
if watchlist == None:
  watchlist = Document.ActiveFilteringSelectionReference.Visuals.AddNew[HtmlTextArea]()
  watchlist.Title = 'Watchlist'

# Headers for the watchlist table
headers = ['Well Name', 'Status', 'Above MRTLL', 'Constraint', 'Stability', 'Offline Prediction']

# HTML Styles
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

# Creating title and beginning of table
html_content += '<h2>' + satellite + '</h2>' 

# Create the table
html_content += '<table>'
# Generate the table headers
html_content += '<tr>'
for h in headers:
  html_content += '<th class="gray">' + h + '</th>'
html_content += '</tr>'

# Must sort the wells based on the rank in descending order
# Higher the rank the higher the priority
wells = sorted(wells, key=lambda k: k['rank'], reverse=True)
for w in wells:
  html_content += '<tr>'
  html_content += htmlName(w)
  html_content += htmlStatus(w)
  html_content += htmlMrtll(w)
  html_content += htmlConstraint(w)
  html_content += htmlStability(w)
  html_content += htmlPeriod(w)
  html_content += '</tr>'

html_content += '</table>'
watchlist.HtmlContent = html_content
