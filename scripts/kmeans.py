"""
Class: KMeansClustering

Implements K-Means Clustering Algorithm, given 2D values as arrays and number
of clusters (k).

"""
from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
from System import Random
import math

class KMeansClustering:
  def __init__(self, x_values, y_values, k, iterations=1000):
    self.k = k
    # Initialises the points and sets the centroids to -1
    self.points = zip(x_values, y_values, [-1]*len(x_values))
    self.centroids = []
    self.max_iterations = iterations
    
  # Runs the algorithm
  def run(self):
    self.initialise_centroids()
    old_centroids = [[0,0]]*self.k
    iterations = 0
    while ((iterations < self.max_iterations) & 
           (self.centroid_difference(old_centroids) != 0)):
      # Need to perform a deep copy since each element contains another object
      old_centroids = self.dcopy_centroids()
      self.assign_points_to_centroid()
      self.calculate_new_centroids()
      iterations += 1
    return self.centroids
  
  # initalises centroids to random values between (0.0, 1.0]
  def initialise_centroids(self):
    # When created it will be seed based on current time
    rand = Random()
    for i in range(0,self.k):
      self.centroids.append([rand.NextDouble(), rand.NextDouble()])
  
  # Returns the absolute difference between the old centroids and the new centroids  
  def centroid_difference(self, old_centroids):
    difference = 0
    for i in range(0, len(old_centroids)):
      difference += abs(old_centroids[i][0]-self.centroids[i][0])
      difference += abs(old_centroids[i][1]-self.centroids[i][1])
    
    return difference
    
  # Returns the ecludiean distance between two points
  def euclidean_distance(self, p1, p2):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )
  
  # Assigns points to centroids
  # The centroid with smallest euclidean distance to a point is assigned
  # to the point
  def assign_points_to_centroid(self):
    for i, point in enumerate(self.points):
      distance = float("inf")
      for j, centroid in enumerate(self.centroids):
        if self.euclidean_distance(point, centroid) < distance:
          distance = self.euclidean_distance(point, centroid)
          # Tuples are immutable which is why we must create a new one
          self.points[i] = (point[0], point[1], j)
  
  # Calculates the new centroid positions, by assigning it the
  # average of each point
  def calculate_new_centroids(self):
    for i, centroid in enumerate(self.centroids):
      sum_x, sum_y, n = 0, 0, 0
      for j, point in enumerate(self.points):
        if point[2] == i:
          sum_x += point[0]
          sum_y += point[1]
          n += 1
      if n > 0:
        self.centroids[i][0] = sum_x/n
        self.centroids[i][1] = sum_y/n

  # Returns a deep copy of the centroids
  def dcopy_centroids(self):
    copy = []
    for centroid in self.centroids:
      copy.append((centroid[0], centroid[1]))
    return copy

# Get the data table (object that contains all data)
data_table = Document.Data.Tables
data_table_name = [table.Name for table in data_table][0]
data_table = data_table[ data_table_name ]

# Getting a reference to the scatter plot
scatter_plot = None
for visual in Document.ActivePageReference.Visuals:
  if "ScatterPlot" in str(visual.TypeId):
    scatter_plot = visual.As[ScatterPlot]()

# Selecting the filtered rows for line calculations
# Creating the cursors to use in our column selections
columns = data_table.Columns
slope_cursor = DataValueCursor.Create(columns["SLOPE"])
gas_rate_cursor = DataValueCursor.Create(columns["GAS_RATE_MSCF_PD"])
days_cursor = DataValueCursor.Create(columns["NUMBER_OF_DAYS_PRODUCED"])

# Creating a row selection that allows us to only get the rows that match
# the current filtering options
filtering = Document.ActiveFilteringSelectionReference
# The selection needs to be converted to an Enumerable type to be used in GetRows
row_selection = filtering.GetSelection(data_table).AsIndexSet()

# Extracting values from columns
slope, gas_rate, days = [], [], []

for each in data_table.GetRows(row_selection, slope_cursor, gas_rate_cursor, days_cursor):
  if str(slope_cursor.CurrentValue) != '-1.#IND':
    slope.append(slope_cursor.CurrentValue)
    gas_rate.append(gas_rate_cursor.CurrentValue)
    days.append(days_cursor.CurrentValue)

# Now using kmeans to work out centroids
kmeans = KMeansClustering(slope, gas_rate, 3)
centroids = kmeans.run()