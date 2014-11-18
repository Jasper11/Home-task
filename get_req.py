#!user/bin/env python
# Creating get request.
import requests
import json
#r = requests.get('http://qainterview.cogniance.com/candidates')
#print(r.text)
def postCandidate(candidateName, candidatePosition):
	url = 'http://qainterview.cogniance.com/candidates'
	payload = {'name': candidateName, 'position': candidatePosition}
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	print(r.text)	
	return;

postCandidate('jasper', 'rider' );
postCandidate('dred', 'judge');
