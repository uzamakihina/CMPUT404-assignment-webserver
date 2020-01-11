#  coding: utf-8 
import socketserver
import os, sys


# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Joe Xu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py



#location, len

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def safe_path(self,basedir,path,follow_symlinks=True):

      

        if follow_symlinks:

            
            return os.path.realpath(path).startswith(basedir)



    def handle(self):
    
        self.data = self.request.recv(1024).strip()
        temp = str(self.data).split()

        

        if ('GET' in temp[0]):

            
            default = "www"
            url = default+temp[1]

            
           
            code = "200 OK"

            if url[len(url)-1] == '/':
                url += "index.html"

            
            try:
                
                tempdir = open(url,"r")
                
            except:
                
                url+= '/index.html'
                code = "301 Moved Permanently "

            #print(safe_path(default, url, follow_symlinks=True))


            try:
                data = open(url, "r") 
            except:
                #self.request.sendall(bytearray("404",'utf-8'))
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n",'utf-8'))
                return
            

            if not self.safe_path(os.getcwd()+"/www", url):
                
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n",'utf-8'))
                return

            self.request.sendall(bytearray("HTTP/1.1 " + code + "\n",'utf-8'))
            pure = data.read()
            if ".css" in url:
                self.request.sendall(bytearray("Content-Type: text/css\n\n",'utf-8'))
               #self.request.sendall(bytearray("location: url\n\n"))
                if code != "301 Moved Permanently ":
                
                    self.request.sendall(bytearray(pure,'utf-8'))

            if ".html" in url:
                self.request.sendall(bytearray("Content-Type: text/html\n\n",'utf-8'))
                #self.request.sendall(bytearray("location: url\n\n"))
                if code != "301 Moved Permanently ":
                    
                    self.request.sendall(bytearray(pure,'utf-8'))


        
        else:

            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\n",'utf-8'))




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()