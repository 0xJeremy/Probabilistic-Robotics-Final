# from .camera import camera
# from .motor import motor
from time import time
import random

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

class camera():
	def __init__(self):
		pass


class robot():
	def __init__(self, guid):
		self.guid = guid
		self.x = 0
		self.y = 0
		self.camera = camera()
		self.motor = motor()

	def get_motor(self):
		return self.motor

	def get_camera(self):
		return self.camera

	def get_position(self):
		return (self.x, self.y)

class ground_truth():
	def __init__(self, width, height, unit):
		self.width = width
		self.height = height
		self.unit = unit
		self.robots = []
		pass

	def make_robot(self, guid):
		bot = robot(guid)
		bot.x = random.randint(self.unit, self.width-self.unit)
		bot.y = random.randint(self.unit, self.height-self.unit)
		self.robots.append(bot)
		return bot

	def get_positions(self):
		return [bot.get_position() for bot in self.robots]
