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
					'params': self.__action_parser(character)
				}
			elif character == 'm':
				for key in self.actions.keys():
					self.actions[key] = {
						'cmd': shutdown
					}

	def __action_parser(self, character):
		if character == 'w':
			return {
				'direction': 'forward'
			}
		if character == 's':
			return {
				'direction': 'back'
			}
		if character == 'd':
			return {
				'direction': 'turn_right'
			}
		if character == 'a':
			return {
				'direction': 'turn_left'
			}

	def get_action(self, guid):
		if guid in self.actions.keys():
			ret = self.actions[guid]
			self.actions[guid] = None
		else:
			ret = None
		return ret

generator = command_generator()
