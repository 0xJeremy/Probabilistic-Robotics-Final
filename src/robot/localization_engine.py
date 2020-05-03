import numpy as np
from numpy import matrix
from numpy.linalg import pinv
from math import sin, cos, radians

class estimate():
	def __init__(self, guid, x, y, distance):
		self.guid = guid
		self.x = x
		self.y = y
		self.distance = distance
		# TODO: Find heading other relative bot
		# self.angle = angle

SIZE = 200

class localization_engine():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.angle = 0
		self.botmatrix = {}

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

	def localize(self, images):
		self.botmatrix = {}
		for image in images:
			distance = SIZE/image.dimension
			x = distance * cos(radians(image.angle)) + self.x
			y = distance * sin(radians(image.angle)) + self.y
			self.botmatrix[image.guid] = estimate(image.guid, x, y, distance)
