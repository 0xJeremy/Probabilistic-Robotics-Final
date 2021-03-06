from .communication_engine import communication_engine
from .localization_engine import localization_engine
from threading import Thread

class Robot():
	def __init__(self, guid, ip, port, hardware, generator, connect, image_size):
		self.guid = guid
		self.hardware = hardware
		self.action_generator = generator
		self.port = port
		self.connected = connect
		if connect:
			self.socket = communication_engine(guid, ip, port)
		self.localization = localization_engine(guid, self.hardware.x, self.hardware.y, image_size)
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
		if self.connected:
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
			images = self.hardware.take_picture()
			self.localization.localize(images)
		if action['cmd'] is 'localize':
			if self.connected:
				self.socket.write_all_estimates(self.get_writable_estimates())
		if action['cmd'] is 'read_data':
			if self.connected:
				self.localization.update_estimates(self.socket.get_all_estimates())

	def get_self_estimate(self):
		return self.localization.get_self_estimate()

	def get_writable_estimates(self):
		return self.localization.get_writable_estimates()

	def get_estimates(self):
		return self.localization.get_estimates()

	def get_absolute_estimates(self):
		return self.localization.get_absolute_estimates()

	def get_relative_estimates(self):
		return self.localization.get_relative_estimates()

	def connect(self, ports):
		if self.connected:
			self.socket.connect(ports)

	def stop(self):
		self.stopped = True
