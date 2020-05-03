import numpy as np
from numpy import matrix
from numpy.linalg import pinv
from math import sin, cos, radians, sqrt
import copy

class absolute_estimate():
	def __init__(self, guid, x, y, distance, visible=True):
		self.guid = guid
		self.dx = x
		self.dy = y
		self.distance = distance
		self.visible = visible


class estimate():
	LOCAL = 1
	REMOTE = 2
	def __init__(self, guid, x, y, type=LOCAL, visible=True):
		self.guid = guid
		self.dx = x
		self.dy = y
		self.type = type
		self.distance = sqrt(x**2 + y**2)
		self.visible = visible

	def serialize(self):
		return {
			'guid': self.guid,
			'dx': self.dx,
			'dy': self.dy,
			'type': self.type
			'distance': self.distance,
			'visible': self.visible
		}

class relative_estimate():
	def __init__(self, guid, x, y, distance, visible=True):
		self.guid = guid
		self.dx = x
		self.dy = y
		self.distance = distance
		self.visible = visible

	def serialize(self):
		return {
			'guid': self.guid,
			'x': self.x,
			'y': self.y,
			'distance': self.distance,
			'visible': self.visible
		}

class remote_estimate():
	def __init__(self, e):
		self.x = e

def deserialize_estimate(e):
	return estimate(e['guid'], e['x'], e['y'], e['distance'], e['visible'])

SIZE = 200

class localization_engine():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.angle = 0
		self.estimates = {}
		self.absolute_estimates = {}
		self.relative_estimates = {}
		self.botmatrix = {}
		self.seen = {}

	def get_self_estimate(self):
		return self.x, self.y

	def update(self, x, y, angle):
		self.x += x
		self.y += y
		self.angle += angle
		self.angle %= 360

	def get_estimates(self):
		return self.estimates.values()

	def get_absolute_estimates(self):
		return self.absolute_estimates.values()

	def get_relative_estimates(self):
		self.absolute_estimates = {}
		for key in self.absolute_estimates.keys():
			absolute = self.absolute_estimates[key]
			rel_x = absolute - self.x
			rel_y = absolute - self.y
			distance = absolute.distance
			visible = absolute.visible
			self.relative_estimates[key] = relative_estimate(rel_y, rel_y, distance, visible)
		return self.absolute_estimates.values()

	def localize(self, images):
		for key in self.estimates:
			self.estimates[key].visible = False
		for image in images:
			distance = SIZE/image.dimension
			x = distance * cos(radians(image.angle))
			y = distance * sin(radians(image.angle))
			self.estimates[image.guid] = estimate(image.guid, x, y)

	def update_estimates(self, estimates):
		self.seen = {}
		print("Estimates: {}".format(estimates))
		for estimate in estimates:
			e = estimate['estimates']
			self.seen[estimate['guid']] = []
			for item in e:
				self.seen[estimate['guid']].append(deserialize_estimate(item))
		print(self.seen)
