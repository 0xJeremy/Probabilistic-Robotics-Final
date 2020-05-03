class command_generator():
	def __init__(self, num_bots):
		self.current_guid = 0
		self.actions = {i:None for i in range(num_bots)}

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
			elif character == 'p':
				self.actions[self.current_guid] = {
					'cmd': 'picture'
				}
			elif character == 'm':
				for key in self.actions.keys():
					self.actions[key] = {
						'cmd': 'read_data'
					}
			elif character == 'l':
				self.actions[self.current_guid] = {
					'cmd': 'localize'
				}

	def __action_parser(self, character):
		action = {
			'w': 'forward',
			's': 'backward',
			'd': 'turn_right',
			'a': 'turn_left'
		}[character]
		return {
			'direction': action
		}

	def get_action(self, guid):
		if guid in self.actions.keys():
			ret = self.actions[guid]
			self.actions[guid] = None
		else:
			ret = None
		return ret
