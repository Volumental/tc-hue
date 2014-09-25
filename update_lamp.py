from phue import Bridge
from tc import TeamCityRESTApiClient
import datetime
import json

class Color:	
	def __init__(self, color_string):
		assert len(color_string) == 7
		assert color_string[:1] == '#'
		self.r = int(color_string[1:3], 16)
		self.g = int(color_string[3:5], 16)
		self.b = int(color_string[5:7], 16)
		
		r = self.r / 255.0
		g = self.g / 255.0
		b = self.b / 255.0
		rgbmin = min(r, g, b)
		rgbmax = max(r, g, b)
		rgb_range = rgbmax - rgbmin

		self.luminance = (rgbmin + rgbmax) / 2.0
		if self.luminance < 0.5:
			self.saturation = rgb_range / (rgbmax + rgbmin)
		else:
			self.saturation = rgb_range / (2.0 - rgbmax - rgbmin)
	
		if r == rgbmax:
			hue = (g - b) / rgb_range
		if g == rgbmax:
			hue = 2.0 + (b - r) / rgb_range
		if b == rgbmax:
			hue = 4.0 + (r - g) / rgb_range
		
		self.hue = hue * 60.0
		
def set_color(bridge, color):
	lights = bridge.get_light_objects()
	for light in lights:
		light.brightness = color.luminance * 254
		light.hue = color.hue * 65535 / 360
		light.saturation = color.saturation * 254

def on(bridge):
	lights = bridge.get_light_objects()
	for light in lights:
		light.on = True

def off(bridge):
	lights = bridge.get_light_objects()
	for light in lights:
		light.on = False

def create_team_city_client(config):
	tc = config[u'teamcity']
	return TeamCityRESTApiClient(
		tc[u'user'], tc[u'password'],
		tc[u'host'], int(tc[u'port']))

def create_bridge(host):
	return Bridge(host)

def update_lamps(config, now):

	bridge = create_bridge(config[u'bridge'][u'host'])
	bridge.connect()
	bridge.get_api()

	today20 = now.replace(hour=20, minute=0, second=0, microsecond=0)
	today06 = now.replace(hour=6, minute=0, second=0, microsecond=0)

	if now > today06 and now < today20:

		tc = create_team_city_client(config)
		all_projects = tc.get_all_projects().get_from_server()

		watched = config[u'teamcity'][u'watch'];

		ok_projects = []
		for p in all_projects[u'project']:
			id = p[u'id'];
			project = tc.get_project_by_project_id(id).get_from_server()
	
			if id in watched:
				statuses = []	
				for build_type in project[u'buildTypes'][u'buildType']:
					b = tc.get_all_builds().set_build_type(build_type[u'id']).set_lookup_limit(1).get_from_server()
					if u'build' in b:
						status = b[u'build'][0][u'status']
						statuses.append(status)
		
				ok_projects.append(not 'FAILURE' in statuses)

		on(bridge)
		if all(ok_projects):
			set_color(bridge, Color(config[u'colors'][u'success']))
		else:
			set_color(bridge, Color(config[u'colors'][u'fail']))
	else:
		off(bridge)


def main():
	with open('config.json') as config_file:    
		config = json.load(config_file)

	update_lamps(config, datetime.datetime.now());


if __name__ == "__main__":
    main()
