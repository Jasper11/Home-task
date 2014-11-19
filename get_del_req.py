#!user/bin/env python
# Creating get request.
import requests
import json
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

get_candidates();

def test_get_candidates():
	r = get_candidates();
	if (r.status_code == 200) and (r.text !=''):
		print 'test passed'
	else:
		print 'test failed'
	return;

#test_get_candidates();

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
	print(r.text)
	#print(r.status_code)
	return r;

#post_candidate('Baba jaga', 'rider', 'application/json' );

def delete_candidate_by_id(user_id):
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.delete (url + str(user_id))
	return r;

#delete_candidate_by_id(25);

def test_post_candidate():
	r = post_candidate('robert' , 'reader', 'application/json');
	if (r.status_code == 201) and (r.text !=''):
		print 'test passed'
	else:
		print 'test failed'
	return;

#test_post_candidate();

def test_get_by_id():
	# preparing
	response = post_candidate('rabbit' , 'zlo', 'application/json');
	json_data = json.loads(response.text)
	id = json_data['candidate']['id']
	
	# testing
	r = get_candidate_by_id(id);
	json_data2 = json.loads(r.text)
	id2 = json_data2 ['candidate']['id']
	
	# checking
	if (id == id2) and (r.status_code == 200):
		print 'test passed'
	else:
		print 'test failed'
	# cleaning
	d = delete_candidate_by_id(id);
	print(id,id2)
	print 'status code', (r.status_code)
	return;

#test_get_by_id();

def test_delete_by_id():
	#preparing	
	p = post_candidate('Romeo', 'worker', 'application/json');
	json_data = json.loads(p.text)
	id = json_data ['candidate']['id']
	#testing	
	d = delete_candidate_by_id(id);
	#checking
	g = get_candidate_by_id(id);
	if (g.status_code != 200):
		print 'test passed'
	else:
		print 'test failed'
	return;

#test_delete_by_id();

def test_post_candidate2():
	#preparing
	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate('Kaka', 'footballman','application/json');
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	if len(g2_cand_list) == len(g_cand_List) + 1 and (p.status_code == 201):
		print 'test passed'
	else:
		print 'test failed'
	print(len(g_cand_List))
	print(len(g2_cand_list))
	print(p.status_code)
	return;

test_post_candidate2(); 
