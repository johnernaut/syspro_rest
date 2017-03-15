""" Tests for the SysproRest API """
import pytest
import vcr
from syspro_rest import SysproRest, APIError

@pytest.fixture()
def syspro_client():
    """ Default valid syspro object """
    syspro = SysproRest(url='http://cg5.caldwellgroup.us:20001/SYSPROWCFService/rest',
                        operator='Michael',
                        operator_pass='',
                        company='A')
    return syspro


@vcr.use_cassette('tests/vcr_cassettes/login-failure.yml')
def test_api_login_invalid():
    """ Tests an invalid API call to login to Syspro """
    with pytest.raises(APIError, message="Expecting APIError"):
        SysproRest(url='http://cg5.caldwellgroup.us:20001/SYSPROWCFService/rest',
                   operator='Michael',
                   operator_pass='1436',
                   company='A')

@vcr.use_cassette('tests/vcr_cassettes/login-success.yml')
def test_api_login_valid(syspro_client):
    """ Tests a valid API call to login to Syspro """
    assert len(syspro_client.user_token) > 0

@vcr.use_cassette('tests/vcr_cassettes/system-information.yml')
def test_system_information(syspro_client):
    """ tests getting system information """
    system_info = syspro_client.system_information()
    assert len(system_info) > 0

@vcr.use_cassette('tests/vcr_cassettes/logon-profile.yml', match_on=['host',
                                                                     'method'])
def test_logon_profile(syspro_client):
    """ tests getting the current users logon profile """
    logon_profile = syspro_client.get_logon_profile()
    assert logon_profile['UserInfo']['CompanyId'] != None
