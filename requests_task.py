#!user/bin/env python
# Creating get request.
import requests
import json
import pytest
def get_candidates():
	url = 'http://qainterview.cogniance.com/candidates'
	r = requests.get(url)
	#data =json.loads(r.text)
	#candidateList = data['candidates']
	#print candidateList[0]['id']
	#print len(candidateList)
	#print(r.text)
	#print(r.status_code)
	return r;

#get_candidates();

def get_candidate_by_id(user_id):
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.get(url + str(user_id))
	return r;

#get_candidate_by_id(18);
#get_candidate_by_id(3);

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
	#print(json.dumps(payload))
	#print(headers)
	#print(r.text)
	#print(r.status_code)
	return r;

#post_candidate('Baba jaga', 'rider', 'application/json' );

def delete_candidate_by_id(user_id):
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.delete (url + str(user_id))
	return r;

#delete_candidate_by_id(25);

def test_get_candidates():
	g = get_candidates();
	assert g.status_code == 200 and g.text !=''

def test_post_candidate():
	r = post_candidate('robert' , 'reader', 'application/json');
	assert r.status_code == 201 and r.text !=''
	
def test_get_by_id():
	# preparing
	g = get_candidates();
	g_data = json.loads(g.text)
	cand_list = g_data['candidates']

	p = post_candidate('rabbit' , 'zlo', 'application/json');
			
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	cand_list2 = g2_data['candidates']
	candidate = [item for item in cand_list2 if item not in cand_list][0]
	
	
	# testing
	g_id = get_candidate_by_id(candidate['id']);
	json_data = json.loads(g_id.text)
	candidate2 = json_data
#	print p.text
#	print g_id.text
	#print cand_list[0]
	#print candidate2['candidate']

	# checking
	assert candidate == candidate2['candidate'] and g_id.status_code == 200

	# cleaning
	d = delete_candidate_by_id(candidate['id']);
	
#test_get_by_id();

def test_delete_by_id():
	#preparing
	g = get_candidates();
	g_data = json.loads(g.text)
	cand_list = g_data ['candidates']
	
	p = post_candidate('Romeo', 'worker', 'application/json');

	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	cand_list2 = g2_data ['candidates']
	candidate = [item for item in cand_list2 if item not in cand_list][0]
	
	#testing	
	d = delete_candidate_by_id(candidate['id']);
	#checking
	g3 = get_candidates();
	g3_data = json.loads(g3.text)
	cand_list3 = g3_data['candidates']
	assert candidate not in cand_list3 and d.status_code == 200

#test_delete_by_id();

def test_post_candidate2():
	#preparing
	cand_name = 'Kristi'
	cand_position = 'dancer'
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name , cand_position ,cont_type);
		
	#checking
	#use difference of cand_lists (A) to check correctness of cand data .
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	candidate = [item for item in g2_cand_list if item not in g_cand_List][0] 
	assert candidate['name']== cand_name  and candidate['position'] == cand_position and (p.status_code == 201)
	
	#cleaning
	d = delete_candidate_by_id(candidate['id']);
	
	#print(len(g_cand_List))
	#print(len(g2_cand_list))
	#print(p.status_code)
	#print p.text
	#print A[0]
	#return;

#test_post_candidate2(); 
