import socket
import datetime



def writeLog(packetData):
    reqLog = open('log.txt', 'a')
    date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
    reqLog.write(date)
    reqLog.write(packetData)
    reqLog.write('\n\n\n\n\n\n')
    reqLog.close()

def main():
    serverReceive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverReceive.bind(('localhost',80))
    serverReceive.listen(5)

    while(True):
        print('waiting...')
        (clientsocket, address) = serverReceive.accept()

        data = clientsocket.recv(8192).decode("utf-8")
        writeLog(data)


        unauthorized = b'HTTP/1.1 401 Unauthorized\nContent-Type: text/html\nServer:Apache\n\n<HTML><h1>UNAUTHORIZED</h1></HTML>'

        clientsocket.sendall(unauthorized)

        clientsocket.close()


        

        if (data == 'cl0se'):
            break
        
    serverReceive.close()
    

if __name__ == "__main__":
    main()
