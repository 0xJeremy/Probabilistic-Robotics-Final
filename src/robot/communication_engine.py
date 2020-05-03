from socketengine import hub
from json import dumps

CHANNEL = 'estimates'

class communication_engine():
	def __init__(self, guid, addr, port):
		self.guid = guid
		self.addr = addr
		self.port = port
		self.names = 0
		self.socket = hub(port)

	def connect(self, ports):
		connections = self.socket.getConnections()
		conn_ports = [c.port for c in connections]
		for port in ports:
			if port not in conn_ports and port != self.port:
				self.socket.connect(str(self.names), self.addr, port)
				self.names += 1
				print("Connected")

	def write_all_estimates(self, estimates):
		text = [e.serialize() for e in estimates]
		data = dumps({
			'guid': self.guid,
			'estimates': text
		})
		print("Writing {}".format(data))
		self.socket.write_all(CHANNEL, data)

	def get_all_estimates(self):
		e = self.socket.get_all(CHANNEL)
		print("Reading: {}".format(e))
		return e

	def close(self):
		self.socket.close()
