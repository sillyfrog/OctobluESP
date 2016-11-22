#!/usr/bin/env python

import socket
import os, sys

UUID = os.environ['UUID']
TOKEN = os.environ['TOKEN']

CONNECT = '<stream:stream xmlns="jabber:client" xmlns:stream="http://etherx.jabber.org/streams" version="1.0" to="meshblu.octoblu.com">'
AUTH = '<auth xmlns="urn:ietf:params:xml:ns:xmpp-sasl" mechanism="PLAIN">%s</auth>'
SUBSCRIBE = '<iq to="meshblu-xmpp.octoblu.com" type="set" id="thissubscription"><request><metadata><jobType>CreateSubscription</jobType><toUuid>%s</toUuid></metadata><rawData>{"subscriberUuid":"%s","emitterUuid":"%s","type":"message.received"}</rawData></request></iq>'

SERVER_STATUS = '<iq to="meshblu-xmpp.octoblu.com" type="get"><request><metadata><jobType>GetStatus</jobType></metadata></request></iq>'

def waitfor(s, waitstr):
    d = ''
    while waitstr not in d:
        read = s.recv(1)
        if not read:
            sys.exit(1)
        d += read
    return d

def main():
    s = socket.socket()
    s.connect(('meshblu-xmpp.octoblu.com', 5222))
    s.send(CONNECT)
    print `waitfor(s, '</stream:features>')`
    print

    auth64 = '%s@meshblu.octoblu.com\x00%s\x00%s' % (UUID, UUID, TOKEN)
    # encode put in new lines by default, so remove them
    auth64 = auth64.encode('base64').replace('\n', '')
    s.send(AUTH % (auth64))
    print `waitfor(s, '/>')`
    print


    s.send(SUBSCRIBE % (UUID, UUID, UUID))
    print `waitfor(s, '</iq>')`

    while 1:
        waitfor(s, '<raw-data>')
        print waitfor(s, '</raw-data>')


if __name__ == '__main__':
    main()

