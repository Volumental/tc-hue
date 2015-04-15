from update_lamp import update_lamps
import json
from datetime import datetime

class PrintAlarm:
	def trigger(self):
		print "Alarm triggered"


class NoLight:
	def __init__(self, id):
		self.light_id = id
		self.brightness = 0
		self.hue = 0
		self.saturation = 0

class NoBridge:
	def connect(self):
		pass

	def get_api(self):
		pass

	def get_light_objects(self):
		return [NoLight(0)]


def _create_no_bridge(host):
	return NoBridge()


def main():
	with open('config.json') as config_file:
		config = json.load(config_file)
	update_lamps(config, datetime.now(), PrintAlarm(), _create_no_bridge)


if __name__ == "__main__":
    main()
