from threading import Thread

class visualizer():
	def __init__(self, ip, port, ground_truth):
		self.stopped = False
		pass

	def start(self):
		Thread(target=self.run, args=()).start()
		return self

	def run(self):
		while True:
			if self.stopped:
				return

	def stop(self):
		self.stopped = True
