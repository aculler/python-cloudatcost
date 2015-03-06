# Python API Wrapper for cloudatcost.com

LIST_SERVERS_URL = "https://panel.cloudatcost.com/api/v1/listservers.php"
LIST_TEMPLATES_URL = "https://panel.cloudatcost.com/api/v1/listtemplates.php"
LIST_TASKS_URL = "https://panel.cloudatcost.com/api/v1/listtasks.php"
POWER_OPERATIONS_URL = "https://panel.cloudatcost.com/api/v1/powerop.php"
CONSOLE_URL = "https://panel.cloudatcost.com/api/v1/console.php"

import requests

class CACPy:
	"""Base class for making requests to the cloud at cost API."""

	def __init__(self,email,api_key):
		self.email = email
		self.api_key = api_key

	def _make_request(self,url,options=dict(),type="GET"):
		data = {
			'key':		self.api_key,
			'login':	self.email
		}

		for key in options:
			data[key] = options[key]

		print "URL: " + str(url)
		print "Data: " 
		print data

		ret = None
		if type == "GET":
			ret = requests.get(url,params=data)
		elif type == "POST":
			ret = requests.post(url,data=data)
		else:
			raise Exception("InvalidRequestType: " + str(type))

		return ret.json()

	def _commit_power_operation(self,server_id,operation):
		options = {'sid': server_id,'action':operation}
		return self._make_request(POWER_OPERATIONS_URL,options=options,type="POST")

	def get_server_info(self):
		jdata = self._make_request(LIST_SERVERS_URL)
		return jdata['data']

	def get_template_info(self):
		jdata = self._make_request(LIST_TEMPLATES_URL)
		return jdata['data']

	def get_task_info(self):
		jdata = self._make_request(LIST_TASKS_URL)
		return jdata['data']

	def power_on_server(self,server_id):
		return self._commit_power_operation(server_id,'poweron')

	def power_off_server(self,server_id):
		return self._commit_power_operation(server_id,'poweroff')

	def reset_server(self,server_id):
		return self._commit_power_operation(server_id,'reset')

	def get_console_url(self,server_id):
		options = {'sid': server_id}
		ret_data = self._make_request(CONSOLE_URL,options=options,type="POST")
		return ret_data['console']
