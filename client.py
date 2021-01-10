import os
import sys
import urllib.request

HOST = '127.0.0.1'
PORT = 65432
while(True):
    args = input().split()
    while(len(args) != 2):
        print("The format is GET site1/filename.extension")
        args = input().split()

    command = args[0]
    while(command != "GET"):
        print('only GET command is supported')
        command = input()
    path = args[1]
    url = "http://127.0.0.1:65432/"+path
    fileName = str(os.path.basename(path))

    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))
    else:
        fileRec =  conn.read()
        f = open(fileName,"wb")
        f.write(fileRec)
        f.close()
        print('Download finished')