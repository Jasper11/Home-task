
Home-task
=========

Requirements
------------
### Platform
- Debian, Ubuntu

How to install and run
-----------------
### python 2.7.3
Check that python interpreter is installed, if not - install python. 

### python_pip 1.5.6
Install pip from repository or manually from http://pip.readthedocs.org/en/latest/installing.html#install-pip


### Requests library
Install Requests (usually it has to be installed at once with pip, but if not -> `pip install requests`)
Manually variant -- [`Install Requests`](http://docs.python-requests.org/en/latest/user/install/#install) 


### pytest 2.6.4  (package for python)
Install pytest package via command  `pip install -U pytest`

### python client for redis
Install via command: `sudo pip install redis`

### install Redis on localmachine
how to install and run Redis is described here: http://redis.io/download 

### running the test
1) Run Redis server (database) in screen using: `$ src/redis-server &`

2) Run the script redis_data.py  via command: `python redis_data.py` - in order to fill the Redis database with needed information.

3) Run the script `py.test requests_task.py`

### running the datamining script for DATAMINING task
Run the script using this command:
`cat datamining.log | python requests_stat.py > datamining_converted.log`
