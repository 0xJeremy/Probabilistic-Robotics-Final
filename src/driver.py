from robot.robot import Robot
from user.visualizer import visualizer
from simulator.ground_truth import ground_truth
from json import loads

with open('config.json', 'r') as f:
	config = loads(f.read())

def initialize_bots(gt):
	global config
	bots = []
	for i in range(config['num_bots']):
		sim = gt.make_robot(guid=i)
		bot = Robot(guid=i,
					ip=config['bots']['ip'],
					port=config['bots']['s_port']+i,
					motor=sim.get_motor(),
					camera=sim.get_camera()
			  )
		bots.append(bot)
	return bots

if __name__ == '__main__':
	try:
		gt = ground_truth(width=config['sim']['width'],
						  height=config['sim']['height'],
						  unit=config['sim']['unit'])
		viz = visualizer(ip=config['viz']['ip'],
						 port=config['viz']['port'],
						 ground_truth=gt).start()
		bots = initialize_bots(gt)
		for bot in bots:
			bot.step()
		while True:
			if viz.stopped:
				break
			pass

	except KeyboardInterrupt as e:
		print(e)
		[bot.stop() for bot in bots]
		viz.stop()

	finally:
		print("Ending simulation...")
		[bot.stop() for bot in bots]
		viz.stop()
