import requests
import pytest
import config



def test_workout_categories():
    w = requests.get(url=config.url_workouts_categories)
    assert w.status_code == 200
    assert w != ''
    for item in w:
		assert 'id' in item
		assert 'caloriePerMinute' in item
		assert 'name' in item

def test_view_workouts_by_id():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=config.url_view_workout + str(uuid) + '/workout/' + str(config.workout_id))
    assert workouts.status_code == 200
    assert workouts.json() != ''

def test_view_workouts_by_wrong_id():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=config.url_view_workout + str(uuid) + '/workout/' + str(config.wrong_workout_id))
    assert workouts.status_code == 404

def test_view_aggregate_workouts():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=config.url_view_workout + str(uuid) + '/workouts' + config.view_workouts_parameters)
    assert workouts.status_code == 200
    assert workouts.json() != ''

def test_view_aggregate_workouts_invalid_parameters():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.get(url=config.url_view_workout + str(uuid) + '/workouts' + config.view_workouts_invalid_parameters)
    assert workouts.status_code == 400

def test_view_aggregate_workouts_invalid_uuid():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    invalid_uuid = uuid + '1'
    assert uuid is not None
    workouts = r.get(url=config.url_view_workout + str(invalid_uuid) + '/workouts' + config.view_workouts_parameters)
    assert workouts.status_code == 404  # doc mistake? don't match with AR: 403 forbidden;

def test_add_workout_by_xcapture():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid) + '/workout/xcapture', headers=config.header, files=config.files)
    assert workouts.status_code == 200  # is code mistake or not ?

def test_add_workout_by_xcapture_invalid_uuid():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid+'1') + '/workout/xcapture', headers=config.header, files=config.files)
    assert workouts.status_code == 404

def test_edit_manual_workout_invalid_parameters():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts_create = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.create_workout_params)
    new_id = workouts_create.json()['id']
    workouts_edit = r.post(url=config.url_view_workout + str(uuid) + '/workout/' + str(new_id) + config.invalid_manual_parameters)
    assert workouts_edit.status_code == 400

def test_add_workout_by_xcapture_invalid_parameters():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid) + '/workout/xcapture')
    assert workouts.status_code == 400


def test_add_manual_workout():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.create_workout_params)
    workout_id = workouts.json()['id']
    assert workout_id is not None


def test_add_manual_workout_same_workout():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.create_workout_params)
    assert workouts.status_code == 500  # inconsistency with doc

def test_add_manual_workout_invalid_uuid():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid+'1') + '/workout' + config.create_workout_params)
    assert workouts.status_code == 404  # AR 403 forbidden (access denied)


def test_add_manual_workout_invalid_parameters():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.invalid_manual_parameters)
    assert workouts.status_code == 400


def test_edit_manual_workout():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts_create = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.create_workout_params)
    new_id = workouts_create.json()['id']
    workouts_edit = r.post(url=config.url_view_workout + str(uuid) + '/workout/' + str(new_id) + config.create_workout_params)
    assert workouts_edit.status_code == 200

def test_edit_manual_workout_with_not_valid_id():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts_create = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.create_workout_params)
    workouts_edit = r.post(url=config.url_view_workout + str(uuid) + '/workout/' + str(config.wrong_workout_id) + config.create_workout_params)
    assert workouts_edit.status_code == 404

def test_delete_no_workout_by_given_id():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts_delete = r.delete(url=config.url_view_workout + str(uuid) + '/workout/' + str(config.wrong_workout_id))
    assert workouts_delete.status_code == 404


def test_delete_workout_by_id():
    r = requests.Session()
    s = r.post(url=config.url_login, data=config.credentials)
    assert s.status_code == 200
    uuid = s.json()['uuid']
    assert uuid is not None
    workouts_create = r.post(url=config.url_view_workout + str(uuid) + '/workout' + config.create_workout_params)
    new_id = workouts_create.json()['id']
    workouts_delete = r.delete(url=config.url_view_workout + str(uuid) + '/workout/' + str(new_id))
    assert workouts_delete.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])





