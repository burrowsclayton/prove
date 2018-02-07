"""
Class: KMeansClustering

Implements K-Means Clustering Algorithm, given 2D values as arrays and number
of clusters (k).

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

class KMeansClustering:
  # k = number of clusters
  def __init__(self, x_values, y_values, k, iterations=1000):
    self.k = k
    # Initialises the points and sets the centroids index to 0
    # The third variable is an index into the centroid array
    self.points = zip(x_values, y_values, [0]*len(x_values))
    self.centroids = []
    self.max_iterations = iterations
    # Used for data normalisation
    self.min_slope = Double.PositiveInfinity
    self.min_rate = Double.PositiveInfinity
    self.max_slope = Double.NegativeInfinity
    self.max_rate = Double.NegativeInfinity
    self.normalised = False
    
  # Runs the k-means algorithm
  def run(self):
    self.initialise_centroids()
    # Used to keep track of the convergence of our centroids
    old_centroids = [[0,0]]*self.k
    iterations = 0
    while ((iterations < self.max_iterations) & 
           (self.centroid_difference(old_centroids) != 0)):
      # Need to perform a deep copy since each element contains another object
      old_centroids = self.dcopy_centroids()
      self.assign_points_to_centroid()
      self.calculate_new_centroids()
      iterations += 1
    return self.unnormalised_centroids() if self.normalised else self.centroids
  
  # initalises centroids to random values between [0.0, 1.0]
  def initialise_centroids(self):
    # Random class is created on time-dependent seed value
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
      distance = Double.PositiveInfinity
      for j, centroid in enumerate(self.centroids):
        if self.euclidean_distance(point, centroid) < distance:
          distance = self.euclidean_distance(point, centroid)
          # Tuples are immutable which is why we must create a new one
          self.points[i] = (point[0], point[1], j)
  
  # Calculates the new centroid positions, by assigning it the
  # average of each point that is associated with it
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

  # Applies Min-Max/Feature Scaling normalisation techniques
  def minmax_normalise_data(self):
    self.normalised = True
    slope, rate = 0, 1
    # Finding the max and min values of each attribute (slope, rate)
    # Use lambda to allow us to search the entire list at once which will
    # then return a tuple variable. which is why we index the result
    self.max_slope = max(self.points, key=lambda points: points[slope])[slope]
    self.min_slope = min(self.points, key=lambda points: points[slope])[slope]
    self.max_rate = max(self.points, key=lambda points: points[rate])[rate]
    self.min_rate = min(self.points, key=lambda points: points[rate])[rate]

    # Applying the normalisation
    # v' = (v-min(e))/(max(e)-min(e))
    # where min(e) and max(e) are the max and min value of attribute e
    for i, point in enumerate(self.points):
      s = (point[slope]-self.min_slope)/(self.max_slope-self.min_slope)
      r = (point[rate]-self.min_rate)/(self.max_rate-self.min_rate)
      self.points[i] = (s,r,0)

  # Unnormalises the centroid values
  def unnormalised_centroids(self):
    unnormalised_centroids = []
    # Must apply the oppsoite of the normalisation equation
    # v = v'*(max(e) - min(e)) + min(e)
    for centroid in self.centroids:
      s = centroid[0]
      g = centroid[1]
      s = s*(self.max_slope-self.min_slope)+self.min_slope
      g = g*(self.max_rate-self.min_rate)+self.min_rate
      unnormalised_centroids.append((s,g))
    return unnormalised_centroids

# Getting the data table object
table_name = "Monthly Production information link"
data_table = Document.Data.Tables[table_name]

# Getting a reference to the scatter plot
scatter_plot = None
for visual in Document.ActivePageReference.Visuals:
  if "ScatterPlot" in str(visual.TypeId):
    scatter_plot = visual.As[ScatterPlot]()

if scatter_plot == None:
  # If no scatter plot has been created then we will not attempt k-means
  MessageBox.Show("No scatter plot has been detected.\nPlease press ProVe Analysis after selecting a well.\nCheers.", "No Scatter Plot")
else:
  # Creating the cursors to use in our column selections
  # Refer to the DataValueCursor in the Spotfire API
  columns = data_table.Columns
  slope_cursor = DataValueCursor.Create(columns["SLOPE"])
  gas_rate_cursor = DataValueCursor.Create(columns["GAS_RATE_MSCF_PD"])
  days_cursor = DataValueCursor.Create(columns["NUMBER_OF_DAYS_PRODUCED"])

  # Creating a row selection that allows us to only get the rows that match
  # the current filtering options (Field, well name, duplicate, non-zero)
  filtering = Document.ActiveFilteringSelectionReference
  # The selection needs to be converted to an Enumerable type to be used in GetRows
  row_selection = filtering.GetSelection(data_table).AsIndexSet()

  # Extracting values from columns
  slope, gas_rate, days = [], [], []
  for each in data_table.GetRows(row_selection, slope_cursor, gas_rate_cursor, days_cursor):
    # Must make sure that the numbers are valid otherwise it will not work with k-means
    if str(slope_cursor.CurrentValue) != '-1.#IND' and  str(slope_cursor.CurrentValue) != '1.#INF':
      slope.append(slope_cursor.CurrentValue)
      gas_rate.append(gas_rate_cursor.CurrentValue)
      days.append(days_cursor.CurrentValue)

  # Now using kmeans to work out centroids
  kmeans = KMeansClustering(slope, gas_rate, 3)
  # We also want out data to be normalised
  kmeans.minmax_normalise_data()
  centroids = kmeans.run()

  # Finding closest data point to the centroids
  # We will use the data points that map closest to a centroid for use in the line equation
  closest_points = []
  for centroid in centroids:
    index = None
    smallest_diff = Double.PositiveInfinity
    for i,point in enumerate(zip(slope,gas_rate)):
      # The 'closeness' is the euclidean distance between the points and centroids
      diff = math.sqrt((centroid[0] - point[0])**2+(centroid[1] - point[1])**2)
      if diff < smallest_diff:
        smallest_diff = diff
        index = i
    closest_points.append((gas_rate[index], days[index]))

  # Sorted based on the number of days
  # Note: This is dependent on days being the second variable in the tuple
  # We sort based on the number of days because the smallest value of days indicates the point belongs to
  # the slope of a quarter, the second highest belongs to a line with slope 1/2 etc.
  sorted_closest_points = sorted(closest_points, key=lambda closest_points: closest_points[1]) 
  quarter_slope_a = math.exp(math.log(sorted_closest_points[0][0])+0.25*math.log(sorted_closest_points[0][1]))
  half_slope_a = math.exp(math.log(sorted_closest_points[1][0])+0.5*math.log(sorted_closest_points[1][1]))
  one_slope_a = math.exp(math.log(sorted_closest_points[2][0])+1*math.log(sorted_closest_points[2][1]))

  # Creating the line expressions
  # log(y) = log(x)*b+log(a)
  # b is the slope, a is the y-intercept
  quater_slope_expression = "[x]*-.25+log10(" + str(quarter_slope_a) + ")"
  half_slope_expression = "[x]*-.5+log10(" + str(half_slope_a) + ")"
  one_slope_expression = "[x]*-1+log10(" + str(one_slope_a) + ")"

  # Plotting the lines onto the ScatterPlot
  quarter_slope_curve = scatter_plot.FittingModels.AddCurve(quater_slope_expression)
  half_slope_curve = scatter_plot.FittingModels.AddCurve(half_slope_expression)
  one_slope_curve = scatter_plot.FittingModels.AddCurve(one_slope_expression)

  # Naming the cruves
  quarter_slope_curve.Curve.CustomDisplayName = "QUARTER SLOPE"
  half_slope_curve.Curve.CustomDisplayName = "HALF SLOPE"
  one_slope_curve.Curve.CustomDisplayName = "ONE SLOPE"

  # Colouring the curves [A, R, G, B]
  green = Color.FromArgb(255, 0, 255, 0)
  orange = Color.FromArgb(255, 255, 174, 25)
  red = Color.FromArgb(255, 255, 0, 0)
  quarter_slope_curve.Curve.Color = green
  half_slope_curve.Curve.Color = orange
  one_slope_curve.Curve.Color = red

  # Changing the style of each line
  # Defaults to single line
  quarter_slope_curve.Curve.LineStyle = LineStyle().Dot
  half_slope_curve.Curve.LineStyle = LineStyle().Dash
  one_slope_curve.Curve.LineStyle = LineStyle()