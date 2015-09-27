import requests
import pytest
import json

url_login = 'https://qa-int-brand.vm.cogniance.com/np/login'
credentials = {'username': 55445544, 'password': 1212}

def test_np_brand_description():
    r = requests.get('http://dev-netpulse.cogniance.com/np/brand/description')
    assert r.status_code == 200
    response =  r.json()
    print response
    print response['description']
    assert response['description'] == 'NetpulseOne'

def test_see_check_if_login_is_working():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code ==200
    uuid = s.json()['uuid']
    assert uuid is not None



if __name__ == '__main__':
    pytest.main([__file__, '-v'])
