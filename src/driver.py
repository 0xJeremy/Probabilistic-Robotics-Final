from robot.robot import Robot
from json import loads

with open('config.json', 'r') as f:
	config = loads(f.read())

bot = Robot(1, 1, 1, 1, 1)
bot.start()
bot.stop()
