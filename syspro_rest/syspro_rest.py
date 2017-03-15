"""A library that wraps the Syspro REST API's"""
from urllib.parse import urlencode
import xmltodict
from . import requests

class APIError(Exception):
    """ Custom error class """
    pass

class SysproRest(object):
    """ A python interface to the Syspro REST API's """
    def __init__(self, **kwargs):
        self.base_url      = kwargs.get('url', '')
        self.operator      = kwargs.get('operator', '')
        self.operator_pass = kwargs.get('operator_pass', '')
        self.company       = kwargs.get('company', '')
        self.company_pass  = kwargs.get('company_pass', '')

        self.login()

    def login(self):
        """ logs into the Syspro REST service """
        params = {'Operator': self.operator, 'OperatorPassword':
                  self.operator_pass, 'CompanyId': self.company,
                  'CompanyPassword': self.company_pass}

        resp = self._make_request('/Logon', params)
        if 'ERROR' in resp.text:
            raise APIError(resp.text.strip())
        self.user_token = resp.text.strip()

    def system_information(self):
        """ gets the Syspro system information """
        resp = self._make_request('/SystemInformation')
        return resp.text

    def get_logon_profile(self):
        """ gets the current users logon profile """
        params = {'UserId': self.user_token}
        resp = self._make_request('/GetLogonProfile', params)
        return xmltodict.parse(resp.text)

    def _make_request(self, url, parameters=None):
        final_url = self._build_url(url, parameters)
        return requests.get(final_url)

    def _build_url(self, url, params=None):
        new_url = self.base_url + url
        if params and len(params) > 0:
            return new_url + '?' + urlencode(dict((k, v) for k, v in params.items()
                                                  if v is not None))
        return new_url
