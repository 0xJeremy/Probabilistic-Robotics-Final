import numpy as np
from numpy import matrix
from numpy.linalg import pinv
from math import sin, cos, radians, sqrt
import copy

class estimate():
	LOCAL = 1
	REMOTE = 2
	def __init__(self, p_guid, r_guid, x, y, dx, dy, type=LOCAL, visible=True):
		self.personal_guid = p_guid
		self.remote_guid = r_guid
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.type = type
		self.distance = sqrt(x**2 + y**2)
		self.visible = visible

	def islocal(self):
		return self.type == estimate.LOCAL

	def isremote(self):
		return self.type == estimate.REMOTE

	def serialize(self):
		return {
			'personal_guid': self.personal_guid,
			'remote_guid': self.remote_guid,
			'x': self.x,
			'y': self.y,
			'dx': self.dx,
			'dy': self.dy,
			'type': self.type,
			'distance': self.distance,
			'visible': self.visible
		}

SIZE = 200

class localization_engine():
	def __init__(self, guid, x, y):
		self.guid = guid
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

	def get_writable_estimates(self):
		return [e.serialize() for e in self.estimates.values()]

	def get_absolute_estimates(self):
		return self.absolute_estimates.values()

	def get_relative_estimates(self):
		pass

	def localize(self, images):
		for key in self.estimates:
			self.estimates[key].visible = False
		for image in images:
			distance = SIZE/image.dimension
			dx = distance * cos(radians(image.angle))
			dy = distance * sin(radians(image.angle))
			est = estimate(
					p_guid=self.guid,
					r_guid=image.guid,
					x=self.x,
					y=self.y,
					dx=dx,
					dy=dy,
					type=estimate.LOCAL
				)
			self.estimates[image.guid] = est

	def update_estimates(self, estimates):
		self.seen = {}
		for e in estimates:
			est = estimate(
					p_guid=self.guid,
					r_guid=e['personal_guid'],
					x=self.x,
					y=self.y,
					dx=e['x']-self.x,
					dy=e['y']-self.y,
					type=estimate.REMOTE
				)
			self.estimates[e['personal_guid']] = est
