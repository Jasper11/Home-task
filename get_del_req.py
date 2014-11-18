#!user/bin/env python
# Creating get request.
import requests
import json
def get_candidates():
	url = 'http://qainterview.cogniance.com/candidates'
	r = requests.get(url)
	#print(r.text)
	#print(r.status_code)
	return r;

#get_candidates();

def test_get1():
	r = get_candidates();
	if (r.status_code == 200) and (r.text !=''):
		print 'test passed'
	else:
		print 'failed'
	return;

#test_get1();

def get_candidate_by_id(user_id):
	payload = user_id
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.get(url + payload)
	print(r.text)
	print(r.status_code)
	return;

#get_candidate_by_id('18');
#get_candidate_by_id('3');

def post_candidate(candidateName, candidatePosition, contentType):
	url = 'http://qainterview.cogniance.com/candidates'
	#payload = {'name': candidateName, 'position': candidatePosition}
	#payload = dict(name=candidateName, position=candidatePosition)
	payload = dict()
	if candidateName is not None:
		payload['name']=candidateName
	if candidatePosition is not None:
		payload['position']=candidatePosition
	headers = dict() 
	if contentType is not None:
		headers['content-type']=contentType
	#headers = {'content-type': contentType}
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	print(json.dumps(payload))
	print(headers)
	print(r.text)
	print(r.status_code)
	return r;

#post_candidate('Baba jaga', 'rider' );


def test_post_candidate():
	r = post_candidate('robert' , 'reader', 'application/json');
	if (r.status_code == 201) and (r.text !=''):
		print 'test passed'
	else:
		print 'test failed'
	return;

test_post_candidate();

def delete_candidate(cand_id):
	payload = cand_id
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.delete(url + payload)
	print(r.text)
	print(r.status_code)
	return;

#delete_candidate('18');
#delete_candidate('3');
