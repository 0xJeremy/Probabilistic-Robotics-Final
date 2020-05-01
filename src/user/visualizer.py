from threading import Thread
import cv2
import numpy as np
import copy
from math import sin, cos, radians

GT_SIZE = 10
EST_SIZE = 10

class visualizer():
	def __init__(self, ip, port, ground_truth, generator):
		self.ip = ip
		self.port = port
		self.gt = ground_truth
		self.generator = generator
		self.width = self.gt.width
		self.height = self.gt.height
		self.unit = self.gt.unit
		self.stopped = False
		self.frame = np.zeros((self.width,self.height,3), np.uint8)
		for i in range(int(self.width/self.unit)):
			u = i*self.unit
			cv2.line(self.frame, (u, 0), (u, self.width), (100, 100, 100), 1, 1)
			cv2.line(self.frame, (0, u), (self.height, u), (100, 100, 100), 1, 1)

	def start(self):
		Thread(target=self.run, args=()).start()
		return self

	def run(self):
		while True:
			if self.stopped:
				cv2.destroyAllWindows()
				return
			key = cv2.waitKey(1)
			if key == ord('q'):
				self.stop()
			self.generator.give_key(key)
			frame = self.generate_frame()
			cv2.imshow("Simulator", frame)

	def generate_frame(self):
		frame = copy.deepcopy(self.frame)
		positions = self.gt.get_positions()
		for pos in positions:
			x = int(pos[0])
			y = int(pos[1])
			cv2.circle(frame, (x, y), GT_SIZE, (255, 0, 0), -1)
			angle = radians(pos[2])
			x += int(cos(angle)*10)
			y += int(sin(angle)*10)
			cv2.circle(frame, (x, y), int(GT_SIZE/2), (0, 0, 255), -1)

		return frame

	def stop(self):
		self.stopped = True
