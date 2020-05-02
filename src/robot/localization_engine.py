import numpy as np
from numpy import matrix
from numpy.linalg import pinv

class localization_engine():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.angle = 0

	def get_self_estimate(self):
		return (self.x, self.y)

	def kalman_filter(self):
		# (Mu Bar) Kalman Filter Belief
		x = A*x + B*u

		# (Sigma Bar) Kalman Filter Belief
		P = A*P*A.T + R

		S = Ct*P*Ct.T + Q
		K = (PCt.T) * pinv(S)

		y = Z - (Ct*x)

		# Mu
		x = x + (K*y)

		# Sigma T
		P = (I - (K*Ct))*P

	def update(self, x, y, angle):
		self.x += x
		self.y += y
		self.angle += angle

	def localize(self, image_direction, image_size):
		pass
