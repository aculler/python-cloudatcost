# Python API Wrapper for cloudatcost.com

import requests

BASE_URL = "https://panel.cloudatcost.com/api/"
API_VERSION = "v1"

LIST_SERVERS_URL = "/listservers.php"
LIST_TEMPLATES_URL = "/listtemplates.php"
LIST_TASKS_URL = "/listtasks.php"
POWER_OPERATIONS_URL = "/powerop.php"
CONSOLE_URL = "/console.php"
RENAME_SERVER_URL = "/renameserver.php"
REVERSE_DNS_URL = "/rdns.php"


class CACPy:
    """Base class for making requests to the cloud at cost API."""

    def __init__(self, email, api_key):
        """Return a CACPy object.

        Required Arguments:
        email - The email address used to authenticate to the API.
        api_key - The key generated in the CAC panel to access the API.
        """
        self.email = email
        self.api_key = api_key

    def _make_request(self, endpoint, options=dict(), type="GET"):
        data = {
            'key': self.api_key,
            'login': self.email
        }

        # Add any passed in options to the data dictionary to be included
        # in the web request.
        for key in options:
            data[key] = options[key]

        url = BASE_URL + API_VERSION + endpoint

        ret = None
        if type == "GET":
            ret = requests.get(url, params=data)
        elif type == "POST":
            ret = requests.post(url, data=data)
        else:
            raise Exception("InvalidRequestType: " + str(type))

        return ret.json()

    def _commit_power_operation(self, server_id, operation):
        options = {
            'sid': server_id,
            'action': operation
        }
        return self._make_request(POWER_OPERATIONS_URL,
                                  options=options,
                                  type="POST")

    def get_server_info(self):
        """Return an array of dictionaries containing server details.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-servers
        """
        return self._make_request(LIST_SERVERS_URL)

    def get_template_info(self):
        """Return an array of dictionaries containing template information.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-templates
        """
        return self._make_request(LIST_TEMPLATES_URL)

    def get_task_info(self):
        """Return an array of dictionaries containing task information.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-tasks
        """
        return self._make_request(LIST_TASKS_URL)

    def power_on_server(self, server_id):
        """Request that the server specified be powered on.

        Required Arguments:
        server_id - The unique ID assaciated with the server to power on.
                    Specified by the 'sid' key returned by get_server_info()

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'poweron')

    def power_off_server(self, server_id):
        """Request that the server specified be powered off.

        Required Arguments:
        server_id - The unique ID associated with the server to power off.
                    Specified by the 'sid' key returned by get_server_info()

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'poweroff')

    def reset_server(self, server_id):
        """Request that the server specified be power cycled.

        Required Arguments:
        server_id - The unique ID associated with the server to power off.
                    Specified by the 'sid' key returned by get_server_info()

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'reset')

    def rename_server(self, server_id, new_name):
        """Modify the name label of the specified server.

        Required Arguments:
        server_id - The unique ID associated with the server to change the
                    label of. Specified by the 'sid' key returned by
                    get_server_info()
        new_name - String to set as the name label.

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#rename-server
        """
        options = {
            'sid': server_id,
            'name': new_name
        }
        return self._make_request(RENAME_SERVER_URL,
                                  options=options,
                                  type="POST")

    def change_hostname(self, server_id, new_hostname):
        """Modify the hostname of the specified server.

        Required Arguments:
        server_id - The unique ID associated with the server to change the
                    hostname of. Specified by the 'sid' key returned by
                    get_server_info()
        new_hostname - Fully qualified domain name to set for the host

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#modify-reverse-dns
        """
        options = {
            'sid': server_id,
            'hostname': new_hostname
        }
        return self._make_request(REVERSE_DNS_URL,
                                  options=options,
                                  type="POST")

    def get_console_url(self, server_id):
        """Return the URL to the web console for the server specified.

        Required Arguments:
        server_id - The unique ID associated with the server you would
                    like the console URL for.
        """
        options = {
            'sid': server_id
        }
        ret_data = self._make_request(CONSOLE_URL,
                                      options=options,
                                      type="POST")
        return ret_data['console']
