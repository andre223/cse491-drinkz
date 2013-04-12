import sys
import _mypath

import random
import socket
import time
from drinkz.app import SimpleApp

s = socket.socket()
host = socket.gethostname()
port = random.randint(8000,9999)
s.bind((host, port))

print 'Starting server on', host, port


s.listen(5)
while True:
    c, addr = s.accept()
    print 'Got connection from', addr

    data = c.recv(1024) # recieve the GET request

    d = {}
    def my_start_response(s, h, return_id=d):
        d['status'] = s
        d['headers'] = h

    app_obj = SimpleApp() # create app object
        
    if data[:3] == "GET":
        status = "HTTP/1.0 "
        environ = {}
        if '/recipesList' in data[4:]:
            environ['PATH_INFO'] = '/recipesList' #put request into path info
        elif '/inventoryList' in data[4:]:
            environ['PATH_INFO'] = '/inventoryList'
        elif '/liquorTypes' in data[4:]:
            environ['PATH_INFO'] = '/liquorTypes'
        elif '/convertToML' in data[4:]:
            environ['PATH_INFO'] = '/convertToML'
        elif '/addRecipe' in data[4:]:
            environ['PATH_INFO'] = '/addRecipe'
        elif '/addType' in data[4:]:
            environ['PATH_INFO'] = '/addType'
        elif '/addInventory' in data[4:]:
            environ['PATH_INFO'] = '/addInventory'
        elif '/' in data[5:]:
            environ['PATH_INFO'] = '/'
        else:
            environ['PATH_INFO'] = '/error'

        html = app_obj(environ, my_start_response)
        status += d['status']
        status +='\n'

        headers = d['headers']

        print 'STATUS----  ', status
        print 'HEADERS----  ', headers
        
        c.send(status)  #send status and headers
        c.send(html[0])
    else:
        c.send("Wrong Format.")
        c.send("GET /[destination]")

    c.close()
