import json
import string
import re
import binascii

def main():
    dataFile = open("SocketLog.txt", "r+")
    writeFile = open("parsed_log_year_month_day.json", "w+")

    lines = dataFile.readlines()
    writeFile.write('[')

    i=0
    payloadCount = 0
    jsonString = ''
    acceptEncodeDone = 0
    acceptFound = 0
    requestFound = 0

    for x in lines:
        # JSON does not support extra quotations or single back slashes
        # This line removed souble quotations
        x = x.translate({ord(c): None for c in '"'})
        # This line replaces any backslashes with double backslashes
        x = x.translate({ord(c): "\\\\" for c in '\\'})
        line = x.split(' ')
        match line[0]:
            case 'Date:':
                i += 1
                acceptEncodeDone = 0
                acceptFound = 0
                requestFound = 0
                if(payloadCount>0):
                    jsonString += (']')
                    payloadCount = 0
                if(i>1):
                    jsonString += ('},')
                    writeFile.write(jsonString + '\n')
                jsonString = '{'
                jsonString += (f'"id": {i}')
                jsonString += (f', "Date": {{"Day of Week": "{line[1]}", "Day of Month": {line[2]}, "Month": "{line[3]}", "Year": {line[4][0:4]}, "Time": "{line[5][:-1]}"}}')
            case 'Client':
                jsonString += (f', "Client Socket": "{line[8][:-2]}"')
            case 'Address:':
                jsonString += (f', "Address": {{"IP": "{line[1][2:-2]}", "Socket": {line[2][:-2]}}}')
                requestNext = 1
            case 'GET' | 'POST' | 'PUT' | 'CONNECT' | 'HEAD' | 'PRI':
                jsonString += (f', "Request Type": "{line[0]}", "Requested": "{line[1]}", "HTTP Version": "{line[2][:-1]}"')
                requestFound = 1
            case 'Host:' | 'host:':
                jsonString += (f', "Host": "{line[1][:-1]}"')
            case 'User-agent:' | 'User-Agent:' | 'user-agent:':
                jsonString += (f', "User-Agent": "{x[12:-1]}"')
            case str(y) if 'AS:' in y:
                jsonString += (f', "AS:": "{x[3:-1]}"')
            case str(y) if 'HL:' in y:
                jsonString += (f', "HL:": "{x[3:-1]}"')
            case 'Referer:':
                jsonString += (f', "Referer": "{x[9:-1]}"')
            case 'Accept:' | 'accept:':
                if(acceptFound == 0):
                    j=0
                    jsonString += (f', "Accept":[')
                    ctSplit = x[8:-1].split(';')
                    for l in ctSplit:
                        if(j>0):
                            jsonString += (', ')
                        jsonString += (f'"{l.strip()}"')
                        j+=1
                    jsonString += (']')
                    acceptFound = 1
                else:
                    pass
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
            case 'Accept-Encoding:' | 'accept-encoding:':
                if(acceptEncodeDone == 0):
                    j=0
                    jsonString += (f', "Accept-Encoding":[')
                    ctSplit = x[16:-1].split(',')
                    for l in ctSplit:
                        if(j>0):
                            jsonString += (', ')
                        jsonString += (f'"{l.strip()}"')
                        j+=1
                    jsonString += (']')
                    acceptEncodeDone = 1
                else:
                    pass
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
            case 'Content-Type:' | 'Content-type:':
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
            case 'X-Presto-Catalog:':
                jsonString += (f', "X-Presto-Catalog": "{x[18:-1]}"')
            case 'X-Presto-Schema:':
                jsonString += (f', "X-Presto-Schema": "{x[17:-1]}"')
            case 'X-Presto-Source:':
                jsonString += (f', "X-Presto-Source": "{x[17:-1]}"')
            case 'X-Presto-User:':
                jsonString += (f', "X-Presto-User": "{x[15:-1]}"')
            case 'X-Trino-Catalog:':
                jsonString += (f', "X-Trino-Catalog": "{x[17:-1]}"')
            case 'X-Trino-Schema:':
                jsonString += (f', "X-Trino-Schema": "{x[16:-1]}"')
            case 'X-Trino-Source:':
                jsonString += (f', "X-Trino-Source": "{x[16:-1]}"')
            case 'X-Trino-User:':
                jsonString += (f', "X-Trino-User": "{x[14:-1]}"')
            case 'X-Forwarded-For:':
                jsonString += (f', "X-Forwarded-For": "{x[17:-1]}"')
            case 'Upgrade-Insecure-Requests:':
                jsonString += (f', "Upgrade-Insecure-Requests": "{x[27:-1]}"')
            case 'Authorization:':
                jsonString += (f', "Authorization": "{x[15:-1]}"')
            case 'BS_REAL_IP:':
                jsonString += (f', "BS_REAL_IP": "{x[12:-1]}"')
            case 't3':
                jsonString += (f', "t3:": "{x[3:-1]}"')
            case str(y) if 'MGLNDD' in y:
                jsonString += (f', "MGLNDD": "{x[0:-1]}"')
            case 'DNT:' | 'Dnt:':
                jsonString += (f', "DNT": "{x[5:-1]}"')
            case 'Sec-GPC:' | 'Sec-Gpc:':
                jsonString += (f', "Sec-GPC": "{x[9:-1]}"')
            case 'Sec-Fetch-Dest:':
                jsonString += (f', "Sec-Fetch-Dest": "{x[16:-1]}"')
            case 'Sec-Fetch-Mode:':
                jsonString += (f', "Sec-Fetch-Mode": "{x[16:-1]}"')
            case 'Sec-Fetch-Site:':
                jsonString += (f', "Sec-Fetch-Site": "{x[16:-1]}"')
            case 'TE:':
                jsonString += (f', "TE": "{x[4:-1]}"')
            case 'SOAPAction:':
                jsonString += (f', "SOAPAction": "{x[12:-1]}"')
            case 'OPTIONS':
                jsonString += (f', "OPTIONS sip": "{x[12:-1]}"')
            case 'Via:':
                jsonString += (f', "Via": "{x[4:-1]}"')
            case 'From:':
                jsonString += (f', "From": "{x[6:-1]}"')
            case 'To:':
                jsonString += (f', "To": "{x[4:-1]}"')
            case 'Call-ID:':
                jsonString += (f', "Call-ID": "{x[9:-1]}"')
            case 'CSeq:':
                jsonString += (f', "CSeq": "{x[6:-1]}"')
            case 'Max-Forwards:':
                jsonString += (f', "Max-Forwards": "{x[14:-1]}"')
            case 'Contact:':
                jsonString += (f', "Contact": "{x[9:-1]}"')
            case 'Origin:':
                jsonString += (f', "Origin": "{x[7:-1]}"')
            case 'Keep-Alive:':
                jsonString += (f', "Keep-Alive": "{x[12:-1]}"')
            case _:
                if(line[0] != '\n'):
                    if(payloadCount == 0):
                        jsonString += (f', "Payload": [')
                    else:
                        jsonString += (f',')
                    printable = all(chars in string.printable for chars in x[:-1])
                    if(printable):
                        jsonString += (f'"{x[:-1]}"')
                    else:
                        jsonString += (f'"{binascii.hexlify(x[:-1].encode('utf-8'))}"')
                        
                    payloadCount += 1
                else:
                    pass

    if(payloadCount>0):
        jsonString += (']')
    jsonString += ('}')
    writeFile.write(jsonString)
    writeFile.write(']')

    dataFile.close()
    writeFile.close()

if __name__ == "__main__":
    main()
