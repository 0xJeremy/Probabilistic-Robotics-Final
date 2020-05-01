from socketengine import hub

class communication_engine():
	def __init__(self, id, addr, port):
		self.addr = addr
		self.port = port
		self.id = id
		self.names = 0
		self.socket = hub(port)

	def connect(self, ports):
		connections = self.socket.getConnections()
		conn_ports = [c.port for c in connections]
		for port in ports:
			if port not in conn_ports and port != self.port:
				self.socket.connect(str(self.names), self.addr, port)
				self.names += 1

	def close(self):
		self.socket.close()
