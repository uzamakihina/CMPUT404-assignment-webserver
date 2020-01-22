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

    

    def not_found(self):
        
        nf_img = open("NotFound.html","r").read()
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
        self.request.sendall(bytearray("Content-Type: text/html; charset=UTF-8\r\n",'utf-8'))
        self.request.sendall(bytearray("Content-Length: " +str(len(nf_img))+"\r\n",'utf-8'))
        self.request.sendall(bytearray("Connection: close\r\n\r\n",'utf-8'))
        self.request.sendall(bytearray(nf_img,'utf-8'))
        
        
        

        #self.request.sendall(bytearray("404 Not Found!",'utf-8'))

    # function to detect depth attacks
    def safe_path(self,highest,dest,follow_symlinks=True):
        if follow_symlinks:
            return os.path.realpath(dest).startswith(highest)



    def handle(self):

        

        #print("reached")

        self.data = self.request.recv(1024).strip()
        temp = str(self.data).split()

        #print(temp)

        # if its a get api
        if ('GET' in temp[0]):
            
            default = "www"
            url = default+temp[1]

            code = "200 OK"

            # if not specific files called
            if url[len(url)-1] == '/':
                url += "index.html"
                


            # if its a 301 
            elif os.path.isdir(url):
                
                code = "301 Moved Permanently"
        


            # if fails to open definitly 404
            try:
                if "301" in code:
                    data = open(url+"/index.html","r")
                else:

                    data = open(url, "r") 
            except:
    
                self.not_found() 
                self.request.close()
                
                return
            

            # is the path higher than www? 
            if not self.safe_path(os.getcwd()+"/www", url):
                
                self.not_found()
                self.request.close()
                
                return

            # send header
            
            pure = data.read()
            
            if ".css" in url:
                self.request.sendall(bytearray("HTTP/1.1 " + code + "\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/css\r\n",'utf-8'))
                self.request.sendall(bytearray("Connection: close\r\n\r\n", 'utf-8'))
                # if code != "301 Moved Permanently ":
                self.request.sendall(bytearray(pure,'utf-8'))
                self.request.close()

            elif ".html" in url or "301" in code:

                
                self.request.sendall(bytearray("HTTP/1.1 " + code + "\r\n",'utf-8'))
                

                if "301" in code:
                    loc = url[3:]+'/'
                    self.request.sendall(bytearray("Location: http://127.0.0.1:8080" + loc + "\r\n", 'utf-8'))
                    
                    self.request.sendall(bytearray("Connection: close\r\n\r\n", 'utf-8'))
                    self.request.close()
                    return
                    
                else:
                    loc = url[3:]
                
                length = str(len(pure))
                #self.request.sendall(bytearray("Location: http://127.0.0.1:8080" + loc + "\r\n", 'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/html; charset=UTF-8\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Length: " + length + "\r\n", 'utf-8'))
                self.request.sendall(bytearray("Connection: close\r\n\r\n", 'utf-8'))
                
                self.request.sendall(bytearray(pure,'utf-8'))
                self.request.close()

                
                
            else:
                # dont give files that are not css or html
                self.not_found()
                self.request.close()
 
        # if not a GET
        else:
            na_img = open("NotAllowed.html","r").read()
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/html; charset=UTF-8\r\n",'utf-8'))
            self.request.sendall(bytearray("Content-Length: " +str(len(na_img))+"\r\n",'utf-8'))
            self.request.sendall(bytearray("Connection: close\r\n\r\n", 'utf-8'))
            self.request.sendall(bytearray(na_img,'utf-8'))
            self.request.close()

        
        
        



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()





    