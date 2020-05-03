import numpy as np
from numpy import matrix
from numpy.linalg import pinv
from math import sin, cos, radians

class estimate():
	def __init__(self, guid, x, y, distance, visible=True):
		self.guid = guid
		self.x = x
		self.y = y
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

def deserialize_estimate(e):
	return estimate(e['guid'], e['x'], e['y'], e['distance'], e['visible'])

SIZE = 200

class localization_engine():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.angle = 0
		self.botmatrix = {}
		self.seen = {}

	def get_self_estimate(self):
		return (self.x, self.y)

	# def kalman_filter(self):
	# 	# (Mu Bar) Kalman Filter Belief
	# 	x = A*x + B*u

	# 	# (Sigma Bar) Kalman Filter Belief
	# 	P = A*P*A.T + R

	# 	S = Ct*P*Ct.T + Q
	# 	K = (PCt.T) * pinv(S)

	# 	y = Z - (Ct*x)

	# 	# Mu
	# 	x = x + (K*y)

	# 	# Sigma T
	# 	P = (I - (K*Ct))*P

	def update(self, x, y, angle):
		self.x += x
		self.y += y
		self.angle += angle
		self.angle %= 360

	def get_estimates(self):
		return self.botmatrix.values()

	def get_absolute_estimates(self):
		estimates = self.botmatrix.values()
		for e in estimates:
			e.x += self.x
			e.y += self.y
		return estimates

	def localize(self, images):
		for key in self.botmatrix:
			self.botmatrix[key].visible = False
		for image in images:
			distance = SIZE/image.dimension
			x = distance * cos(radians(image.angle))
			y = distance * sin(radians(image.angle))
			self.botmatrix[image.guid] = estimate(image.guid, x, y, distance)

	def update_estimates(self, estimates):
		self.seen = {}
		for estimate in estimates:
			e = estimate['estimates']
			self.seen[estimate['guid']] = []
			for item in e:
				self.seen[estimate['guid']].append(deserialize_estimate(item))
		print(self.seen)
