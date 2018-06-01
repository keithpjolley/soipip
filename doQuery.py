# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import socket
import login
import doMessages
import statusMessage
from constants import *

def queryGateway(gatewayIP, gatewayPort):
  # cut/paste from python manual
  tcpSock = None
  for res in socket.getaddrinfo(gatewayIP, gatewayPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
      tcpSock = socket.socket(af, socktype, proto)
    except OSError as msg:
      tcpSock = None
      continue
    try:
      tcpSock.connect(sa)
    except OSError as msg:
      tcpSock.close()
      tcpSock = None
      continue
    break

  if tcpSock is None:
    sys.stderr.write("ERROR: {}: Could not open socket to gateway host.\n".format(me))
    sys.exit(10)

  with tcpSock:
    connectString = b'CONNECTSERVERHOST\r\n\r\n'  # not a string...
    tcpSock.sendall(connectString)
    # the gateway does not respond to the connect message. don't wait for something here because you aren't going to get it

    # tx/rx challenge  (?)  (gateway returns its mac address in the form 01-23-45-AB-CD-EF) why? dunno.
    tcpSock.sendall(doMessages.makeMessage(code.CHALLENGE_QUERY))
    data = tcpSock.recv(48)
    if not data:
      sys.stderr.write("WARNING: {}: no {} data received.\n".format(me, "CHALLENGE_ANSWER"))
    rcvcode, data = doMessages.decodeMessage(data)
    if(rcvcode != code.CHALLENGE_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, CHALLENGE_ANSWER))
      sys.exit(10)
   
    # two steps to building messages - build the data then add the header

    msg = login.createLoginMessage()
    tcpSock.sendall(doMessages.makeMessage(code.LOCALLOGIN_QUERY, msg))
    data = tcpSock.recv(48)
    if not data:
      sys.stderr.write("WARNING: {}: no {} data received.\n".format(me, "LOCALLOGIN_ANSWER"))
    rcvcode, data = doMessages.decodeMessage(data)
    if(rcvcode != code.LOCALLOGIN_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode2, code.LOCALLOGIN_ANSWER))
      sys.exit(10)
    # response should be empty

    tcpSock.sendall(doMessages.makeMessage(code.VERSION_QUERY))
    data = tcpSock.recv(480)
    if not data:
      sys.stderr.write("WARNING: {}: no {} data received.\n".format(me, "VERSION_ANSWER"))
    rcvcode, data = doMessages.decodeMessage(data)
    if(rcvcode != code.VERSION_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode2, code.VERSION_ANSWER))
      sys.exit(10)
    print(doMessages.getMessageString(data))

    tcpSock.sendall(doMessages.makeMessage(code.POOLSTATUS_QUERY, struct.pack("<I", 0)))
    rcvcode, data = doMessages.decodeMessage(tcpSock.recv(480))
    if(rcvcode != code.POOLSTATUS_ANSWER):
      sys.stderr.write("WARNING: {}: rcvCode2({}) != {}.\n".format(me, rcvCode2, code.POOLSTATUS_ANSWER))
      sys.exit(11)
    print(statusMessage.decodeStatusMessage(data))
