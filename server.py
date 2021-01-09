import socket
import os
import threading

HOST = '127.0.0.1'
PORT = 65432

def makeHttpOKResponse(filePath):
    pdf_file = open(filePath,'rb')
    fileSizeStr = str(os.path.getsize(filePath))
    response = 'HTTP/1.1 200 OK\r\n\
            \r\nContent-Length: '+fileSizeStr+'\r\nContent-Type: application/octet-stream;\
            \r\nContent-Disposition: attachment; filename='+str(os.path.basename(filePath))+'\r\n\
            \r\nConnection: Closed\r\n\r\n'
    response = response.encode()+pdf_file.read()
    return response

failResponse = b'HTTP/1.1 404 Not found\r\n\
            \r\nContent-Length: 49\r\nContent-Type: text/html\
            \r\nConnection: Closed\r\n\r\n<html><body><h1>File not found</h1></body></html>'

def connHandler(conn,addr):
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        l = data.split()
        filePath = l[1][1:]
        print("file path is ", filePath)
        if(os.path.exists(filePath)):
            response = makeHttpOKResponse(filePath)
        else:
            response = failResponse
        conn.sendall(response)
    conn.close()

threads = list()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while(True):
        conn, addr = s.accept()
        x=threading.Thread(target=connHandler,args=(conn,addr))
        threads.append(x)
        x.start()

