import requests
import pytest

url_login = 'https://qa-int-brand.vm.cogniance.com/np/login'
url_workouts = 'https://qa-int-brand.vm.cogniance.com/np/exerciser/'
credentials = {'username': 55445544, 'password': 1212}
parameters = '?interval=single&intervalCount=1&startDate=19910101'
invalid_parameters = '?interval=single&startDate=19910101'
workout_id = 4240912
wrong_workout_id = 4240912312
header = {'Content-Type': 'multipart/form-data'}
files = {'file': open('Untitled-1.jpg', 'rb')}
manual_parameters = '?workoutDateTime=2012-09-02T17:00:00-08:00&workoutDateTimeNoTz=1941-01-01+12:45:34&timezone=US/Pacific&category=1&duration=170&calories=130'
invalid_manual_parameters = '?timezone=US/Pacific&category=1&duration=170&calories=130'
manual_parameters_2 = '?workoutDateTime=2012-09-02T17:00:00-08:00&workoutDateTimeNoTz=1991-01-01+12:45:34&timezone=US/Pacific&category=1&duration=170&calories=170'

def test_see_check_if_login_is_working():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None


def test_workout_categories():
    w = requests.get(url='https://qa-int-brand.vm.cogniance.com/np/workout/categories')
    assert w.status_code == 200
    categories = w.json()
    print categories
    assert categories != ''


def test_aggregate_workouts():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=url_workouts + str(uuid) + '/workouts' + parameters)
    assert workouts.status_code == 200
    assert workouts != ''

def test_aggregate_workouts_wrong_data():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=url_workouts + str(uuid) + '/workouts' + invalid_parameters)
    assert workouts.status_code == 400

def test_aggregate_workouts_wrong_uuid():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=url_workouts + str(uuid+'1') + '/workouts' + parameters)
    assert workouts.status_code == 404  # don't match with AR: 403 forbidden; doc mistake?

def test_view_workouts_by_id():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=url_workouts + str(uuid) + '/workout/' + str(workout_id))
    assert workouts.status_code == 200


def test_view_workouts_by_wrong_id():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=url_workouts + str(uuid) + '/workout/' + str(wrong_workout_id))
    assert workouts.status_code == 404

def test_add_workout_by_xcapture_invalid():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=url_workouts + str(uuid) + '/workout/xcapture')
    assert workouts.status_code == 400

def test_add_workout_by_xcapture():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=url_workouts + str(uuid) + '/workout/xcapture', headers=header, files=files)
    assert workouts.status_code == 200

def test_add_manual_workout():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is None
    workouts = r.post(url=url_workouts + str(uuid) + '/workout' + manual_parameters) #change parameters for new workout (time)
    assert workouts.status_code == 200


def test_add_manual_workout_same_workout():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=url_workouts + str(uuid) + '/workout' + manual_parameters)
    assert workouts.status_code == 500 #AR 409 Conflict is it correct ?

def test_add_manual_workout_invalid_uuid():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=url_workouts + str(uuid+'1') + '/workout' + manual_parameters)
    assert workouts.status_code == 404 #AR 403 forbidden (access denied)


def test_add_manual_workout_invalid_parameters():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=url_workouts + str(uuid) + '/workout' + invalid_manual_parameters)
    assert workouts.status_code == 400


def test_edit_manual_workout():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=url_workouts + str(uuid) + '/workout' + manual_parameters)
    new_id = workouts.json()['id'] #change parameters for new workout (change time)
    workouts2 = r.post(url=url_workouts + str(uuid) + '/workout/' + str(new_id) + manual_parameters_2)
    assert workouts2.status_code == 200

def test_delete_workout_by_id_invalid():
    r = requests.Session()
    s = r.post(url=url_login, data=credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.delete(url=url_workouts + str(uuid) + '/workout/' + str(wrong_workout_id))
    assert workouts.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])





