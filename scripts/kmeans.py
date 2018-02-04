"""
Class: KMeansClustering

Implements K-Means Clustering Algorithm, given 2D values as arrays and number
of clusters (k).

"""
from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
import random as r
import math as m
import copy as c

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
      old_centroids = c.deepcopy(self.centroids)
      self.assign_points_to_centroid()
      self.calculate_new_centroids()
      iterations += 1
  
  # initalises centroids to random values between (0.0, 1.0]
  def initialise_centroids(self):
    # Seed it with time to get different seeds each time
    # Otherwise we will always have same random values
    r.seed(None)
    for i in range(0,self.k):
      self.centroids.append([r.random(), r.random()])
  
  # Returns the absolute difference between the old centroids and the new centroids  
  def centroid_difference(self, old_centroids):
    difference = 0
    for i in range(0, len(old_centroids)):
      difference += abs(old_centroids[i][0]-self.centroids[i][0])
      difference += abs(old_centroids[i][1]-self.centroids[i][1])
    
    return difference
    
  # Returns the ecludiean distance between two points
  def euclidean_distance(self, p1, p2):
    return m.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )
  
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

