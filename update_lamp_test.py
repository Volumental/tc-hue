import update_lamp
from mock import Mock

class fake_team_city:
	def __init__(self):
		self.projects = {}
		self.value = None
		self.build_type_filter = None

	def add_project(self, id, configs):
		self.projects[id] = configs
	
	def get_from_server(self):
		return self.value

	def get_all_projects(self):
		self.value = { u'project': [ { u'id': id } for id in self.projects.keys()] }
		return self

	def get_project_by_project_id(self, id):
		p = self.projects[id]
		self.value = { u'buildTypes' : { u'buildType': [ { u'id': id } for id in p.keys()] } }
		return self

	def set_build_type(self, build_type):
		self.build_type_filter = build_type
		return self
	
	def get_all_builds(self):
		self.value = []
		return self

	def set_lookup_limit(self, limit):
		return self

light1 = Mock()
def create_bridge_fake(host):
	bridge = Mock()
	bridge.connect = Mock()

	bridge.get_light_objects.return_value = [light1]
	return bridge

def create_team_city_client_fake(config):
	tc = fake_team_city();
	tc.add_project('a', { 'config_a': True });
	return tc

def main():
	cfg = {
		"bridge": {
			"host": "bridge.acme.com"
		},
		"teamcity": {
			"user": "zelda",
			"password": "secret",
			"host": "teamcity.acme.com",
			"port": "666",
			"watch": ["a", "b"]
		}
	}
	update_lamp.create_bridge = create_bridge_fake
	update_lamp.create_team_city_client = create_team_city_client_fake

	update_lamp.update_lamps(cfg)
	

if __name__ == "__main__":
    main()
