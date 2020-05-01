class command_generator():
	def __init__(self):
		self.current_guid = 0
		self.actions = {}

	def give_key(self, key):
		if key == -1:
			return
		character = chr(key)
		if character.isnumeric():
			self.actions[int(character)] = None
			self.current_guid = int(character)
			print("Changing to bot {}".format(self.current_guid))
		else:
			if character in ['w', 'a', 's', 'd']:
				self.actions[self.current_guid] = {
					'cmd': 'move',
					'key': character
				}
				print("Issueing Command {}".format(character))

	def get_action(self, guid):
		if guid in self.actions.keys():
			ret = self.actions[guid]
			self.actions[guid] = None
		else:
			ret = None
		return ret

generator = command_generator()
