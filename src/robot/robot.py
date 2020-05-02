from .communication_engine import communication_engine
from .localization_engine import localization_engine
from threading import Thread

class Robot():
	def __init__(self, guid, ip, port, hardware, generator):
		self.guid = guid
		self.hardware = hardware
		self.action_generator = generator
		self.port = port
		self.socket = communication_engine(guid, ip, port)
		self.localization = localization_engine()
		self.stopped = False

	def start(self):
		Thread(target=self.run, args=()).start()
		return self

	def run(self):
		while True:
			if self.stopped:
				self.__shutdown()
				return
			self.step()

	def __shutdown(self):
		self.socket.close()

	def step(self):
		action = self.action_generator.get_action(self.guid)
		if action is None:
			return
		if action['cmd'] is 'noop':
			pass
		if action['cmd'] is 'shutdown':
			self.stop()
		if action['cmd'] is 'move':
			x, y, theta = self.hardware.run_for_time(action['params']['direction'])
			self.localization.update(x, y, theta)
		if action['cmd'] is 'picture':
			self.hardware.take_picture()


	def get_estimate(self):
		return self.localization.get_self_estimate()

	def connect(self, ports):
		self.socket.connect(ports)

	def stop(self):
		self.stopped = True
