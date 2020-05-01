from .communication_engine import communication_engine
from .localization_engine import localization_engine
from threading import Thread

class Robot():
	def __init__(self, guid, ip, port, motor, camera):
		self.id = guid
		self.motor = motor
		self.camera = camera
		self.stopped = False

	def start(self):
		Thread(target=self.run, args=()).start()
		return self

	def run(self):
		while True:
			if self.stopped:
				return

	def step(self):
		pass

	def stop(self):
		self.stopped = True
