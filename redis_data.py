#!user/bin/env python

import redis


def dBase_creation():
  d_base = redis.StrictRedis (host='localhost', port=6379, db=0)
  set_candidate_simple_name = d_base.hmset('candidate:simple_name', {'name':'Peter Brown', 'position':'accounter'})
  set_candidate_without_name = d_base.hmset('candidate:without_name', {'position':'dealer'})
  set_candidate_with_name_like_empty_string = d_base.hmset('candidate:with_name_like_empty_string', {'name':'', 'position':'dealer'})
  set_candidate_without_position = d_base.hmset('candidate:without_position', {'name':'Peter Brown'})	
  set_candidate_long_name = d_base.hmset('candidate:long_name', {'name':'ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ', 'position':'accounter'})
  set_candidate_name_like_num = d_base.hmset('candidate:name_like_num', {'name':'1234567890123456789012345678901234567890', 'position':'manager'})
  set_candidate_name_like_special_symbols = d_base.hmset('candidate:name_like_special_symbols', {'name':'!\"#$%&\'()*+,-./:;<=>?@[\\]^_{|}~', 'position':'manager'})
 
  
dBase_creation();