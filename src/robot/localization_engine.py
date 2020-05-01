class localization_engine():
	def __init__(self):
		self.x = 0
		self.y = 0

	def get_self_estimate(self):
		return (self.x, self.y)
