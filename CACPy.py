# Python API Wrapper for cloudatcost.com

LIST_SERVERS_URL = "https://panel.cloudatcost.com/api/v1/listservers.php"
LIST_TEMPLATES_URL = "https://panel.cloudatcost.com/api/v1/listtemplates.php"
LIST_TASKS_URL = "https://panel.cloudatcost.com/api/v1/listtasks.php"
POWER_OPERATIONS_URL = "https://panel.cloudatcost.com/api/v1/poweropp.php"
CONSOLE_URL = "https://panel.cloudatcost.com/api/v1/console.php"

from urllib2 import urlopen
from urllib import urlencode
import json

class CACPy:
	"""Base class for making requests to the cloud at cost API."""

	def __init__(self,email,api_key):
		self.email = email
		self.api_key = api_key

	def _make_request(self,base_url,options=dict(),type="GET"):
		url = base_url
		data = dict()

		if type == "GET":
			url += "?key=" + str(self.api_key) + "&login=" + str(self.email)

			for key in options:
				url += "&" + str(key) + "=" + str(options[key])
		elif type == "POST":
			data = {
				'key':		self.api_key,
				'login':	self.email
			}
			for key in options:
				data[key] = options[key]
		else:
			raise Exception("InvalidRequestType: " + str(type))

		print "URL: " + str(url)
		print "Data: " 
		print data

		try:
			ret = urlopen(url,urlencode(data))
		except:
			print "Status: " + ret['status']
			print "Error Code: " + ret['error']
			print "Description: " + ret['error_description']

		if str(ret.getcode()) != "200":
			raise Exception("Bad return value: " + str(ret))

		ret_data = ret.read()
		return json.loads(ret_data)

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
