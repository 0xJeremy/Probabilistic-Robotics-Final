from robot.robot import Robot
from user.visualizer import visualizer
from user.command_generator import command_generator
from simulator.ground_truth import ground_truth
from json import loads

with open('config.json', 'r') as f:
	config = loads(f.read())

def initialize_bots(gt, generator):
	global config
	bots = []
	for i in range(config['num_bots']):
		sim = gt.get_hardware_instance(guid=i)
		bot = Robot(guid=i,
					ip=config['bots']['ip'],
					port=config['bots']['s_port']+i,
					hardware=sim,
					generator=generator,
					connect=config['bots']['connect'],
					image_size=config['sim']['image_size']
			  )
		bots.append(bot)
	return bots

if __name__ == '__main__':
	try:
		generator = command_generator(config['num_bots'])
		gt = ground_truth(width=config['sim']['width'],
						  height=config['sim']['height'],
						  unit=config['sim']['unit'],
						  speed=config['sim']['speed'],
						  angle=config['sim']['angle'],
						  image_size=config['sim']['image_size'],
						  max_distance=config['sim']['max_distance'],
						  max_angle=config['sim']['max_angle'])
		bots = initialize_bots(gt, generator)
		viz = visualizer(ip=config['viz']['ip'],
						 port=config['viz']['port'],
						 ground_truth=gt,
						 bots=bots,
						 generator=generator)
		if config['viz']['threaded']:
			viz.start()
		ports = [b.port for b in bots]
		[b.connect(ports) for b in bots]
		[b.start() for b in bots]
		while not viz.stopped:
			if not config['viz']['threaded']:
				viz.run()

	except KeyboardInterrupt as e:
		print(e)
		[bot.stop() for bot in bots]
		viz.stop()

	finally:
		print("Ending simulation...")
		[bot.stop() for bot in bots]
		viz.stop()
