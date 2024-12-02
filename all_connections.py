import socket
import datetime
import threading



def writeLog(packetData, clientsocket, address):
    try:
        # Open Log File
        reqLog = open('SocketLog.txt', 'a')

        # Write Date to file
        date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
        reqLog.write(date)

        # Write Client Info
        clientInfo = 'Client Socket: ' + str(clientsocket) + '\nAddress: ' + str(address) + '\n'
        reqLog.write(clientInfo)

        # Write Packet Info
        reqLog.write(packetData)
        reqLog.write('\n\n\n\n\n\n')

        # Close Log File
        reqLog.close()
    except IOError as e:
        print("Write Failed(IOError):\n")
        reqLog = open('WriteFailLog.txt', 'a')
        date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
        reqLog.write(date)
        reqLog.write(str(e))
        reqLog.write('\n\n\n\n\n\n')
        reqLog.close()
    except ConnectionError as e:
        print("Write Failed(ConnectionError)\n")
        reqLog = open('WriteFailLog.txt', 'a')
        date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
        reqLog.write(date)
        reqLog.write(str(e))
        reqLog.write('\n\n\n\n\n\n')
        reqLog.close()
    except TypeError as e:
        print("Write Failed(TypeError):\n")
        reqLog = open('WriteFailLog.txt', 'a')
        date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
        reqLog.write(date)
        reqLog.write(str(e))
        reqLog.write('\n\n\n\n\n\n')
        reqLog.close()
    except Exception as e:
        print("Write Failed(Exception):\n")
        reqLog = open('WriteFailLog.txt', 'a')
        date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
        reqLog.write(date)
        reqLog.write(str(e))
        reqLog.write('\n\n\n\n\n\n')
        reqLog.close()

def bindWrite(serverReceive):

    while(True):
        try:
            (clientsocket, address) = serverReceive.accept()

            data = clientsocket.recv(8192).decode("utf-8")
            writeLog(data, clientsocket, address)


            unauthorized = b'HTTP/1.1 401 Unauthorized\nContent-Type: text/html\nServer:Apache\n\n<HTML><h1>UNAUTHORIZED</h1></HTML>'

            clientsocket.sendall(unauthorized)

            clientsocket.close()
            if (data == 'cl0se'):
                break
        except ConnectionError as e:
            print("Write Failed\n")
            reqLog = open('WriteFailLog.txt', 'a')
            date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
            reqLog.write(date)
            reqLog.write(str(e))
            reqLog.write('\n\n\n\n\n\n')
            reqLog.close()
        except Exception as e:
            print("Write Failed\n")
            reqLog = open('WriteFailLog.txt', 'a')
            date = 'Date: ' + datetime.datetime.now().strftime('%a %d %b %Y, %H:%M:%S' + '\n')
            reqLog.write(date)
            reqLog.write(str(e))
            reqLog.write('\n\n\n\n\n\n')
            reqLog.close()
        
    serverReceive.close()
    
def main():
    server80 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server80.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    server80.bind((socket.gethostname(),80))
    server80.listen(5)
    server591 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server591.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    server591.bind((socket.gethostname(),591))
    server591.listen(5)
    server8008 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server8008.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    server8008.bind((socket.gethostname(),8008))
    server8008.listen(5)
    server8080 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server8080.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    server8080.bind((socket.gethostname(),8080))
    server8080.listen(5)
    
    

    thread80 = threading.Thread(target=bindWrite, args=(server80,))
    thread591 = threading.Thread(target=bindWrite, args=(server591,))
    thread8008 = threading.Thread(target=bindWrite, args=(server8008,))
    thread8080 = threading.Thread(target=bindWrite, args=(server8080,))

    thread80.start()
    thread591.start()
    thread8008.start()
    thread8080.start()

    thread80.join()
    thread591.join()
    thread8008.join()
    thread8080.join()

if __name__ == "__main__":
    main()
