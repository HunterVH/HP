import json

def main():
    dataFile = open("SocketLog.txt", "r+")

    lines = dataFile.readlines()

    #line = lines[0].split(' ')
    i=0
    jsonString = ''

    for x in lines:
        line = x.split(' ')
        match line[0]:
            case 'Date:':
                i += 1
                possiblePayload = 0;
                if(i>1):
                    jsonString += ('},')
                    print(jsonString)
                jsonString = '{'
                jsonString += (f'"id": {i}')
                jsonString += (f', "Date": {{"Day of Week": "{line[1]}", "Day of Month": {line[2]}, "Month": "{line[3]}", "Year": {line[4][0:4]}, "Time": "{line[5][:-1]}"}}')
            case 'Client':
                jsonString += (f', "Client Socket": "INFO"')
            case 'Address:':
                #print(f', "Address": {{"IP": "{line[1][2:-2]}", "Socket": {line[2][:-1]}}}')
                jsonString += (f', "Address": {{"IP": "{line[1][2:-2]}", "Socket": {line[2][:-2]}}}')
                requestNext = 1
            case 'GET' | 'POST' | 'PUT' | 'CONNECT' | 'HEAD' | 'PRI':
                jsonString += (f', "Request Type": "{line[0]}", "Requested": "{line[1]}", "HTTP Version": "{line[2][:-1]}"')
            case 'Host:':
                jsonString += (f', "Host": "{line[1][:-1]}"')
            case 'User-agent:' | 'User-Agent:':
                jsonString += (f', "User-Agent": "{x[12:-1]}"')
            case str(y) if 'AS:' in y:
                jsonString += (f', "AS:": "{x[3:-1]}"')
            case str(y) if 'HL:' in y:
                jsonString += (f', "HL:": "{x[3:-1]}"')
            case 'Referer:':
                jsonString += (f', "Referer": "{x[9:-1]}"')
            case 'Accept:':
                j=0
                jsonString += (f', "Accept":[')
                ctSplit = x[8:-1].split(';')
                for l in ctSplit:
                    if(j>0):
                        jsonString += (', ')
                    jsonString += (f'"{l.strip()}"')
                    j+=1
                jsonString += (']')
            case 'Accept-Charset:':
                j=0
                jsonString += (f', "Accept-Charset":[')
                ctSplit = x[15:-1].split(',')
                for l in ctSplit:
                    if(j>0):
                        jsonString += (', ')
                    jsonString += (f'"{l.strip()}"')
                    j+=1
                jsonString += (']')
            case 'Accept-Encoding:':
                j=0
                jsonString += (f', "Accept-Encoding":[')
                ctSplit = x[16:-1].split(',')
                for l in ctSplit:
                    if(j>0):
                        jsonString += (', ')
                    jsonString += (f'"{l.strip()}"')
                    j+=1
                jsonString += (']')
            case 'Accept-Language:':
                j=0
                jsonString += (f', "Accept-Language":[')
                ctSplit = x[16:-1].split(';')
                for l in ctSplit:
                    if(j>0):
                        jsonString += (', ')
                    jsonString += (f'"{l.strip()}"')
                    j+=1
                jsonString += (']')
            case 'Cache-Control:':
                jsonString += (f', "Cache-Control":"{x[15:-1]}"')
            case 'Pragma:':
                jsonString += (f', "Pragma":"{x[8:-1]}"')
            case 'Proxy-Connection:':
                jsonString += (f', "Proxy-Connection": "{x[18:-1]}"')
            case 'Connection:':
                jsonString += (f', "Connection": "{line[1][:-1]}"')
            case 'Content-Type:':
                j=0
                jsonString += (f', "Content-Type":[')
                ctSplit = x[13:-1].split(';')
                for l in ctSplit:
                    if(j>0):
                        jsonString += (', ')
                    jsonString += (f'"{l.strip()}"')
                    j+=1
                jsonString += (']')
            case 'Content-Length:':
                jsonString += (f', "Content-Length": {line[1][:-1]}')
            case 'Cookie:':
                jsonString += (f', "Cookie": "{x[8:-1]}"')
            case 'X-Requested-With:':
                jsonString += (f', "X-Requested-With": "{x[18:-1]}"')
            case 'Upgrade-Insecure-Requests:':
                jsonString += (f', "Upgrade-Insecure-Requests": "{x[27:-1]}"')
            case 'Authorization:':
                jsonString += (f', "Authorization": "{x[15:-1]}"')
            case 'BS_REAL_IP:':
                jsonString += (f', "BS_REAL_IP": "{x[12:-1]}"')
            case 't3':
                jsonString += (f', "t3:": "{x[3:-1]}"')
            case str(x) if 'MGLNDD' in x:
                jsonString += (f', "MGLNDD": "{x[0:-1]}"')
            case _:
                if(line[0] != '\n'):
                    if(possiblePayload == 1):
                        possiblePayload == 0
                    else:
                        z = 2
                else:
                    possiblePayload = 1;
    
    jsonString += ('}')
    print(jsonString)
    print(']')
    #json.loads(string in question)

    dataFile.close()

if __name__ == "__main__":
    main()
