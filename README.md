# Probabilistic Robotics (Comp-150) Final Project

#### To-Run

To run this simulation, ensure all dependencies (listed below) are installed and compatible with Python3. The main driver is located in the `src` folder and can be run with
```bash
python3 driver.py
```
To change parameters in the simulation, modify `src/config.json`. The configuration file is explained below.

#### Requirements
socket.engine
```bash
pip3 install socket.engine
```
opencv
```bash
pip3 install opencv-python
```
numpy
```bash
pip3 install numpy
```

#### Simulation Control
To control the simulation, use the keyboard. Because the simulation runs more slowly the more bots are added, sometimes the key must be pressed multiple times to register.
```
[0-9]: Select Bot by GUID

w: Move forward 1 translation_unit
s: Move backward 1 translation_unit
d: Rotate left 1 degree_unit
a: Rotate right 1 degree_unit

p: Take picture and localize self to others
l: Report localizations to network
m: Read from network and localize others to self
q: Quit the simulation
```

#### Simulation Configuration
```json
{
	"num_bots": "number of bots in the simulation (int)",
	"viz": {
		"ip": "IP for the visualization to connect with (string)",
		"port": "Port for the visualization to use (int)",
		"threaded": "True/False to multithread the visualization (boolean)"
	},
	"bots": {
		"ip": "IP for the bots to use when connecting (string)",
		"s_port": "Starting port for bot connections (int)",
		"connect": "Specify if the bots should connect to the network (boolean)"
	},
	"sim": {
		"width": "Overall simulation width (int)",
		"height": "Overall simulation height (int)",
		"unit": "Unit size for the simulation (int)",
		"speed": "Speed bots move in the simulation (int)",
		"angle": "Angle with which bots turn (int)",
		"image_size": "Arbitrary image constant (int)",
		"max_distance": "Maximum distance bots can see (int)",
		"max_angle": "Maximum angle bots can see (int)"
}
```

#### Design

![Design specification](https://raw.githubusercontent.com/0xJeremy/Probabilistic-Robotics-Final/master/docs/design.png?token=AJN4KPW32BUQ4C2PNC6TVNS6W3OFE)