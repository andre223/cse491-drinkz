import sys
import _mypath

import random
import socket
import time
from drinkz.app import SimpleApp
from StringIO import StringIO
import simplejson

app_obj = SimpleApp()

s = socket.socket()
host = socket.gethostname()
#host = socket.getfqdn()
port = random.randint(8000,9999)
s.bind((host, port))

print 'Starting server on', host, port


s.listen(5)
while True:
    c, addr = s.accept()
    print 'Got connection from', addr

    buffer = c.recv(1024) 

    while "r\n\r\n" not in buffer:
	data = c.recv(1024)
	if not data:
	    break
	buffer += data
	print (buffer,)
	time.sleep(1)


    print 'Got Request: ', (buffer,)

    lines = buffer.splitlines()
    if(len(lines) < 1):
	print "Bad request"
	continue
    request_line = lines[0]
    print "Lines: ", request_line
    request_type, path, protocol = request_line.split()
    print 'GOT', request_type, path, protocol

    request_headers = lines[1:]
    query = ""
    if '?' in path:
	path, query = path.split('?', 1)

    print request_headers

    environ = {}
    environ['PATH_INFO'] = path
    environ['QUERY_STRING'] = query
    environ['REQUEST_METHOD'] = request_type

    if (request_type == 'POST'):
	'''
	lengthList = [cont for cont in request_headers if "Content-Length" in cont]
	length = lengthList[0]
	numberList = [int(i) for i in length.split() if i.isdigit()]
	number = numberList[0]
	environ['CONTENT_LENGTH'] = number
        '''
	environ['CONTENT_LENGTH'] = len(request_headers[0])
	wsgi_input = request_headers[0]
	environ['wsgi.input'] = StringIO(wsgi_input)


    d = {}
    def my_start_response(s, h):
        d['status'] = s
        d['headers'] = h

    results = app_obj(environ, my_start_response)

    print "Results: ", results
    '''
    response = simplejson.loads(results[0])
    print "Response: ", response
    '''
    response_headers = []
    for k, v in d['headers']:
	h = "%s: %s" % (k,v)
	response_headers.append(h)

    
    if request_type == "POST":
	result_dict = simplejson.loads(results[0])
	result_dict["success"] = True
	response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(simplejson.dumps(result_dict))
    else:
	response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)
    '''
    response = "\r\n".join(response_headers) + "\r\n" + str(response['result'])+"\r\n\r\n" 
    '''
    c.send("HTTP/1.0 %s\r\n" % d['status'])
    c.send(response)
    c.close()





