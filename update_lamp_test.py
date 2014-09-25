import update_lamp
from mock import Mock
import datetime

class fake_team_city:
	def __init__(self, projects):
		self.projects = projects
		self.value = None

	def get_from_server(self):
		return self.value

	def get_all_projects(self):
		self.value = { u'project': [ { u'id': id } for id in self.projects.keys()] }
		return self

	def get_project_by_project_id(self, id):
		p = self.projects[id]
		self.value = { u'buildTypes' : { u'buildType': [ { u'id': id } for id in p.keys()] } }
		return self

	def status(self, success):
		return 'SUCCESS' if success else 'FAILURE'

	def set_build_type(self, build_type):
		self.value = {}
		for id in self.projects:
			for cfg_id in self.projects[id]:
				if cfg_id == build_type:
					s = self.status(self.projects[id][cfg_id]) 
					self.value =  { u'build': [ { u'status': s } ] }
		return self
	
	def get_all_builds(self):
		return self

	def set_lookup_limit(self, limit):
		return self

light1 = Mock()
def create_bridge_fake(host):
	bridge = Mock()
	bridge.connect = Mock()

	bridge.get_light_objects.return_value = [light1]
	return bridge

def assertEqual(expected, actual):
	assert expected == actual, "Expected %s, but was %s" % (expected, actual)

class fixture:
	def __init__(self, cfg):
		self.cfg = cfg
		update_lamp.create_bridge = create_bridge_fake
		self.now = datetime.datetime(2014, 9, 25, 13, 37)

	def test_one_build_failed(self):
		update_lamp.create_team_city_client = lambda config: fake_team_city({ 'a': { 'config_a': False } })
		update_lamp.update_lamps(self.cfg, self.now)
		
		assertEqual(0.0, light1.hue)
		assertEqual(True, light1.on)

	def test_no_builds_fail(self):
		update_lamp.create_team_city_client = lambda config: fake_team_city({ 'a': { 'config_a': True } })
		update_lamp.update_lamps(self.cfg, self.now)

		assertEqual(21845.0, light1.hue)	
		assertEqual(True, light1.on)

def main():
	cfg = {
		"bridge": {
			"host": "bridge.acme.com"
		},
		"colors": {
			"success": "#00ff00",
			"fail": "#ff0000"
		},
		"teamcity": {
			"user": "zelda",
			"password": "secret",
			"host": "teamcity.acme.com",
			"port": "666",
			"watch": ["a", "b"]
		}
	}
	f = fixture(cfg)
	f.test_one_build_failed()
	f.test_no_builds_fail()

if __name__ == "__main__":
    main()

