#!user/bin/env python
import redis
import requests
import json
import pytest

def get_candidates():
	url = 'http://qainterview.cogniance.com/candidates'
	r = requests.get(url)
	return r;

def get_candidate_by_id(user_id):
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.get(url + str(user_id))
	return r;

def post_candidate(candidateName, candidatePosition, contentType):
	url = 'http://qainterview.cogniance.com/candidates'
	payload = dict()
	payload['name']=candidateName
	payload['position']=candidatePosition
	headers = dict() 
	headers['content-type']=contentType
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	return r;

def delete_candidate_by_id(user_id):
	url = 'http://qainterview.cogniance.com/candidates/'
	r = requests.delete (url + str(user_id))
	return r;

def get_not_exist_id():
	g = get_candidates();
	g_data = json.loads(g.text)
	cand_list = g_data['candidates']
	max_id = 0
	for cand in cand_list:
	  user_id = cand['id']
	  if user_id > max_id:
	      max_id = user_id 
	not_exist_id = max_id + 1
	return not_exist_id;
      
class TestGetMethods:
  
  def test_get_candidates(self):
	#testing
	g = get_candidates();
	assert g.status_code == 200 and g.text !=''

  def test_get_by_id(self):
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

	# checking
	assert candidate == candidate2['candidate'] and g_id.status_code == 200

	# cleaning
	d = delete_candidate_by_id(candidate['id']);

  def test_get_by_id_with_not_exist_id(self):
	# preparing
	not_exist_id = get_not_exist_id();
	
	# testing
	response = get_candidate_by_id(not_exist_id);

	# checking
	assert response.status_code != 200 

  def test_get_by_negative_id(self):
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
	g_id = get_candidate_by_id(candidate['id']*(-1));
	
	# checking
	assert g_id.status_code != 200
	#cleaning
	d = delete_candidate_by_id(candidate['id']);

class TestPostMethods:

  def test_post_candidate_simple_name(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:simple_name', 'name')
	cand_position = d_base.hget('candidate:simple_name', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name, cand_position, cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	candidate = [item for item in g2_cand_list if item not in g_cand_List][0] 
	assert candidate['name']== cand_name and candidate['position'] == cand_position and (p.status_code == 201)
	
	#cleaning
	d = delete_candidate_by_id(candidate['id']);

  def test_post_candidate_duplicate_name(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:simple_name', 'name')
	cand_position = d_base.hget('candidate:simple_name', 'position')
	cand_position_2 = cand_position + 'changed'
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name, cand_position, cont_type);
	
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	candidate = [item for item in g2_cand_list if item not in g_cand_List][0]
	
	p2 = post_candidate(cand_name, cand_position_2, cont_type);
			
	#checking
	assert g1_cand_List == g2_cand_list and (p2.status_code != 201)
	
	#cleaning
	g3 = get_candidates();
	g3_data = json.loads(g2.text)
	g3_cand_list = g2_data['candidates']
	if g2_cand_list != g3_cand_list:
	 candidate2 = [item for item in g3_cand_list if item not in g2_cand_List][0]
	 d = delete_candidate_by_id(candidate2['id']);
	d = delete_candidate_by_id(candidate['id']);
	
	
  def test_post_candidate_without_name(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:without_name', 'name')
	cand_position = d_base.hget('candidate:without_name', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name, cand_position, cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	assert g_cand_List == g2_cand_list and (p.status_code == 400)
	#cleaning
	if g1_cand_List != g2_cand_list:
	 candidate = [item for item in g2_cand_list if item not in g_cand_List][0]
	 d = delete_candidate_by_id(candidate['id']);
	

  def test_post_candidate_without_position(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:without_position', 'name')
	cand_position = d_base.hget('candidate:without_position', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name, cand_position, cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	candidate = [item for item in g2_cand_list if item not in g_cand_List][0] 
	assert candidate['name'] == cand_name and candidate['position'] == cand_position and (p.status_code == 201)
	
	#cleaning
	d = delete_candidate_by_id(candidate['id']);

  def test_post_candidate_without_content_type(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:simple_name', 'name')
	cand_position = d_base.hget('candidate:simple_name', 'position')
	cont_type = None

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name, cand_position, cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	assert g_cand_List == g2_cand_list and (p.status_code == 400)

  def test_post_candidate_with_name_like_empty_string(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:with_name_like_empty_string', 'name')
	cand_position = d_base.hget('candidate:with_name_like_empty_string', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name , cand_position ,cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	assert g_cand_List == g2_cand_list and (p.status_code == 400)
	#cleaning
	if g_cand_List != g2_cand_list:
	 candidate = [item for item in g2_cand_list if item not in g_cand_List][0]
	 d = delete_candidate_by_id(candidate['id']);
	
  def test_post_candidate_long_name(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:long_name', 'name')
	cand_position = d_base.hget('candidate:long_name', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name , cand_position ,cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	candidate = [item for item in g2_cand_list if item not in g_cand_List][0] 
	assert candidate['name'] == cand_name and candidate['position'] == cand_position and (p.status_code == 201)
	#cleaning
	d = delete_candidate_by_id(candidate['id']);

  def test_post_candidate_with_name_like_num(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:name_like_num', 'name')
	cand_position = d_base.hget('candidate:name_like_num', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(int(cand_name) , cand_position ,cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	assert g_cand_List == g2_cand_list and (p.status_code != 201)
	#cleaning
	if g_cand_List != g2_cand_list:
	 candidate = [item for item in g2_cand_list if item not in g_cand_List][0]
	 d = delete_candidate_by_id(candidate['id']);

  def test_post_candidate_with_name_like_special_symbols(self):
	#preparing
	d_base = redis.StrictRedis(host='localhost', port=6379, db=0)
	cand_name = d_base.hget('candidate:name_like_special_symbols', 'name')
	cand_position = d_base.hget('candidate:name_like_special_symbols', 'position')
	cont_type = 'application/json'

	g = get_candidates();
	g_data = json.loads(g.text)
	g_cand_List = g_data['candidates']
	
	#testing
	p = post_candidate(cand_name , cand_position ,cont_type);
		
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	g2_cand_list = g2_data['candidates']
	assert g_cand_List == g2_cand_list and (p.status_code != 201)
	#cleaning
	if g_cand_List != g2_cand_list:
	 candidate = [item for item in g2_cand_list if item not in g_cand_List][0]
	 d = delete_candidate_by_id(candidate['id']);
	
	
class TestDeleteMethods:

  def test_delete_by_id(self):
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

  def test_delete_by_id_with_not_exist_id(self):
	#preparing
	g = get_candidates();
	g_data = json.loads(g.text)
	cand_list = g_data ['candidates']
	
	not_exist_id = get_not_exist_id();
		
	#testing	
	d = delete_candidate_by_id(not_exist_id);
			
	#checking
	g2 = get_candidates();
	g2_data = json.loads(g2.text)
	cand_list2 = g2_data['candidates']
	assert cand_list == cand_list2 and d.status_code != 200

  def test_delete_by_negative_id(self):
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
	neg_id = candidate['id']*(-1)
	d = delete_candidate_by_id(neg_id);
	
	#checking
	g3 = get_candidates();
	g3_data = json.loads(g3.text)
	cand_list3 = g3_data['candidates']
	assert cand_list2 == cand_list3 and d.status_code != 200
	#cleaning
	d = delete_candidate_by_id(candidate['id']);
	



 
