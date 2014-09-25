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

def create_team_city_client(config):
	tc = config[u'teamcity']
	return TeamCityRESTApiClient(
		tc[u'user'], tc[u'password'],
		tc[u'host'], int(tc[u'port']))

def create_bridge(host):
	return Bridge(host)

def update_lamps(config):

	bridge = create_bridge(config[u'bridge'][u'host'])
	bridge.connect()
	bridge.get_api()

	now = datetime.datetime.now()
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


def main():
	with open('config.json') as config_file:    
		config = json.load(config_file)

	update_lamps(config);


if __name__ == "__main__":
    main()
