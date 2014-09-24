from phue import Bridge
from tc import TeamCityRESTApiClient
import datetime
import json

def green(bridge):
	lights = bridge.get_light_objects()
	for light in lights:
		light.brightness = 254
		light.hue = 23847
		light.saturation = 250 

def red(bridge):
	lights = bridge.get_light_objects()
	for light in lights:
		light.brightness = 254
		light.hue = 63300
		light.saturation = 250 

def on(bridge):
	lights = bridge.get_light_objects()
	for light in lights:
		light.on = True

def off(bridge):
	lights = bridge.get_light_objects()
	for light in lights:
		light.on = False

with open('config.json') as config_file:    
    config = json.load(config_file)

print config
bridge = Bridge(config[u'bridge'][u'host'])

bridge.connect()
bridge.get_api()

now = datetime.datetime.now()
today20 = now.replace(hour=20, minute=0, second=0, microsecond=0)
today06 = now.replace(hour=6, minute=0, second=0, microsecond=0)

if now > today06 and now < today20:

	#tc = TeamCityRESTApiClient('build-lamp', 'Abc123', 'build.volumental.com', 8111);
	tc = TeamCityRESTApiClient('build-lamp', 'Abc123', 'localhost', 8111);
	all_projects = tc.get_all_projects().get_from_server()

	with open('projects.cfg') as f:
		watched = f.read().splitlines()

	print watched

	ok_projects = []
	for p in all_projects[u'project']:
		id = p[u'id'];
		project = tc.get_project_by_project_id(id).get_from_server()
	
		if id in watched:
			print id
			statuses = []	
			for config in project[u'buildTypes'][u'buildType']:
				b = tc.get_all_builds().set_build_type(config[u'id']).set_lookup_limit(1).get_from_server()
				if u'build' in b:
					status = b[u'build'][0][u'status']
					statuses.append(status)
		
			ok_projects.append(not 'FAILURE' in statuses)


	on(bridge)
	if all(ok_projects):
		green(bridge)
	else:
		red(bridge)
else:
	off(bridge)

