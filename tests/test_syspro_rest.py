""" Tests for the SysproRest API """
import os
import pytest
import vcr
from syspro_rest import SysproRest, APIError

BASE_URL = os.getenv('BASE_URL', None)
OPERATOR = os.getenv('OPERATOR', None)
OPERATOR_PW = os.getenv('OPERATOR_PW', None)
COMPANY = os.getenv('COMPANY', None)
COMPANY_PW = os.getenv('COMPANY_PW', None)

@pytest.mark.skipif(not BASE_URL and not OPERATOR,
                    reason="You must provide a base url and operator")

@pytest.fixture()
def syspro_client():
    """ Default valid syspro object """
    syspro = SysproRest(url=BASE_URL,
                        operator=OPERATOR,
                        operator_pass=OPERATOR_PW,
                        company=COMPANY,
                        company_password=COMPANY_PW)
    return syspro

@pytest.mark.usefixture('syspro_client')
class TestSysproRest:
    @vcr.use_cassette('tests/vcr_cassettes/login-failure.yml')
    def test_api_login_invalid(self):
        """ Tests an invalid API call to login to Syspro """
        with pytest.raises(APIError, message="Expecting APIError"):
            SysproRest(url=BASE_URL,
                       operator='lsdkfjs',
                       operator_pass='lksjdf;lskdfj',
                       company='RANDOM')

    @vcr.use_cassette('tests/vcr_cassettes/login-success.yml')
    def test_api_login_valid(self, syspro_client):
        """ Tests a valid API call to login to Syspro """
        assert len(syspro_client.user_token) > 0

    @vcr.use_cassette('tests/vcr_cassettes/system-information.yml')
    def test_system_information(self, syspro_client):
        """ tests getting system information """
        system_info = syspro_client.system_information()
        assert len(system_info) > 0

    @vcr.use_cassette('tests/vcr_cassettes/logon-profile.yml', match_on=['host',
                                                                         'method'])
    def test_logon_profile(self, syspro_client):
        """ tests getting the current users logon profile """
        logon_profile = syspro_client.get_logon_profile()
        assert logon_profile['UserInfo']['CompanyId'] != None
