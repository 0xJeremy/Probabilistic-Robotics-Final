# from .camera import camera
# from .motor import motor

class motor():
	def __init__(self):
		pass


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

class ground_truth():
	def __init__(self):
		self.robots = []
		pass

	def make_robot(self):
		bot = robot()
		self.robots.append(bot)
		return bot

