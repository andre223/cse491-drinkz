#! /usr/bin/env python

import sys
import socket

def main(args):    
    address = args[1]    
    port = args[2]    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    s.connect((address, int(port)))    
    #s.send("GET / HTTP/1.0\r\n\r\n")
     
    s.send("POST / HTTP/1.0\r\n\r\n")
    buffer = ""
    while 1:        
	buf = s.recv(1000)        
	if not buf:            
	    break
	buffer += buf        
	print buf    

    print 'done'
    s.close()   

if __name__ == '__main__':   
   main(sys.argv)
