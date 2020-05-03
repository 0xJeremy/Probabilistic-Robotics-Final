# from .camera import camera
# from .motor import motor
from time import time
import random
from math import sin, cos, radians, sqrt, atan, degrees

class motor():
	def __init__(self):
		self.encoder = [0, 0]
		self.encoder_enable = [True, True]
		self.run_time = [0, 0]
		self.speed = [0, 0]
		self.reduction_ratio = [1, 1]
		pass

	def set_encoder_enable(self, id):
		for i in id:
			self.encoder_enable[i] = True

	def set_encoder_disable(self, id):
		for i in id:
			self.encoder_enable[i] = False

	def set_reduction_ratio(self, id, ratio):
		for i in id:
			self.reduction_ratio[i] = ratio

	def __calculate_encoder(self, id):
		if self.encoder_enable[id]:
			self.encoder[id] += (time() - self.run_time[id]) * self.reduction_ratio[i]

	def __run(self, id, orientation, speed):
		if speed == 0:
			if self.speed[id] != 0:
				self.__calculate_encoder(id)
			self.speed[id] = 0
		else:
			if orientation != 1 or orientation != -1:
				raise RunTimeError("Orientation not 1 or -1")
			self.speed[id] = orientation*speed
			self.run_time[id] = time()

	def motor_movement(self, id, orientation, speed):
		for i in id:
			self.__run(i, orientation, speed)

	def get_encoder(self, id):
		values = []
		for i in id:
			self.__calculate_encoder(self, i)
			values.append(self.encoder[i])
		return values

	def reset_encoder(self, id):
		for i in id:
			self.encoder[i] = 0

	def motor_stop(self, id):
		for i in id:
			self.__run(i, 0, 0)

class image():
	def __init__(self, guid, dimension, angle_from_center):
		self.guid = guid
		self.dimension = dimension
		self.angle = angle_from_center

def distance(ref, other):
	diff_x = other.x - ref.x
	diff_y = other.y - ref.y
	return sqrt(diff_x**2 + diff_y**2)

def angle(ref, other):
	diff_x = other.x - ref.x
	diff_y = other.y - ref.y
	if diff_y == 0:
		return 0 if diff_x > 0 else 180
	if diff_x == 0:
		return 90 if diff_y > 0 else 270
	if diff_x > 0:
		if diff_y > 0:
			return degrees(atan(diff_y / diff_x))
		return degrees(atan(diff_y / diff_x)) + 360
	return degrees(atan(diff_y / diff_x)) + 180

MAX_DISTANCE = 500
MAX_ANGLE = 45
def visible(ref, other):
	d = distance(ref, other)
	if d > MAX_DISTANCE:
		return False
	a = angle(ref, other)
	diff_angle = a - ref.angle
	if abs(diff_angle) <= MAX_ANGLE:
		return True
	return False

SIZE = 200
def construct_image(ref, other):
	d = distance(ref, other)
	a = angle(ref, other)
	return image(other.guid, SIZE/d, a)

class camera():
	def __init__(self, self_hardware, get_hardware):
		self.hardware = self_hardware
		self.get_hardware = get_hardware

	def take_picture(self):
		ref = self.hardware
		others = self.get_hardware()
		seen = []
		for other in others:
			if ref.guid is other.guid:
				continue
			if visible(ref, other):
				seen.append(construct_image(ref, other))
		return seen

SPEED = 50
ANGLE = 30
class hardware():
	def __init__(self, guid, get_all_hardware):
		self.guid = guid
		self.motor = motor()
		self.camera = camera(self, get_all_hardware)
		self.angle = 0
		self.x = 0
		self.y = 0

	def run_for_time(self, direction):
		diff_x, diff_y, diff_angle = 0, 0, 0
		if direction is 'forward' or direction is 'backward':
			mult = 1 if direction is 'forward' else -1
			diff_x = mult * SPEED * cos(radians(self.angle))
			diff_y = mult * SPEED * sin(radians(self.angle))
		if direction is 'turn_right' or direction is 'turn_left':
			diff_angle = ANGLE if direction is 'turn_right' else -ANGLE
		self.x += diff_x
		self.y += diff_y
		self.angle += diff_angle
		self.angle %= 360
		return diff_x, diff_y, diff_angle

	def get_motor(self):
		return self.motor

	def get_camera(self):
		return self.camera

	def take_picture(self):
		return self.camera.take_picture()

	def get_position(self):
		return (self.x, self.y, self.angle)

	def get_all_data(self):
		return (self.guid, self.x, self.y, self.angle)

	def set_position(self, x, y):
		self.x = x
		self.y = y


STARTING_X = [100, 200]
STARTING_Y = [500, 500]

class ground_truth():
	def __init__(self, width, height, unit):
		self.width = width
		self.height = height
		self.unit = unit
		self.hardware = []
		pass

	def get_hardware_instance(self, guid):
		h = hardware(guid, self.get_all_hardware)
		x = STARTING_X[guid]
		y = STARTING_Y[guid]
		# x = random.randint(self.unit, self.width-self.unit)
		# y = random.randint(self.unit, self.height-self.unit)
		h.set_position(x, y)
		self.hardware.append(h)
		return h

	def get_all_hardware(self):
		return self.hardware

	def get_positions(self):
		return [h.get_position() for h in self.hardware]
