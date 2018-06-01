#! /usr/bin/env python
# -*- coding: UTF8 -*-
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

# find a local gateway.
# see Section 2 of Protocol_Document.pdf for more info.
#
# pushes a broadcast udp datagram
# listens for a response
# decodes response
# returns: (gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk)
#   the first two should be self explanatory.
#   no idea what to do with Type and Subtype.
#   Name is like "Pentair AB-CD-EF" (different than listed in the doc)
#   okchk is a boolean for if the datagram had the correct check digit in it. Not sure what to do if wrong.

import sys
import socket
import struct
import ipaddress
from constants import me

def findGateway(verbose):
  # these are only for the datagram so keep them here instead of "constants.py"
  bcast = "255.255.255.255"
  port  = 1444
  wantchk = 2
  addressfamily = socket.AF_INET

  # no idea why this datastructure... it works.
  data  = struct.pack('<bbbbbbbb', 1,0,0,0, 0,0,0,0)
  # Create a UDP socket
  try:
    udpSock = socket.socket(addressfamily, socket.SOCK_DGRAM)
  except:
    sys.stderr.write("ERROR: {}: socket.socket boarked.\n".format(me))
    sys.exit(1)
  # Get ready to broadcast
  try:
    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  except:
    sys.stderr.write("ERROR: {}: udpSock.setsockopt boarked.\n".format(me))
    sys.exit(2)

  # send the datagram
  if(verbose):
    print("Broadcasting for pentair systems...")
  try:
    udpSock.sendto(data, (bcast, port))
  except:
    sys.stderr.write("ERROR: {}: udpSock.sendto boarked.\n".format(me))
    sys.exit(3)

  # listen for a gateway responding
  if(verbose):
    print("Waiting for a response...")
  try:
    data, server = udpSock.recvfrom(4096)
  except:
    sys.stderr.write("ERROR: {}: udpSock.recvfrom boarked.\n".format(me))
    sys.exit(4)
  try:
    udpSock.close()
  except:
    # not sure we really need to exit if we can't close the socket...
    sys.stderr.write("ERROR: {}: udpSock.close boarked.\n".format(me))
    sys.exit(5)

  # "server" is ip_address:port that we got a response from. 
  # not sure what happens if we have to gateways on a subnet. havoc i suppose.
  if(verbose):
    system, port = server
    print("INFO: {}: Received a response from {}:{}".format(me(), system, port))

  # the format here is a little different than the documentation. 
  # the response I get back includes the gateway's name in the form of "Pentair: AB-CD-EF"
  expectedfmt = "<I4BH2B"
  paddedfmt = expectedfmt + str(len(data)-struct.calcsize(expectedfmt)) + "s"
  try:
    chk, ip1, ip2, ip3, ip4, gatewayPort, gatewayType, gatewaySubtype, gatewayName = struct.unpack(paddedfmt, data)
  except struct.error as err:
    print("ERROR: {}: received unpackable data from the gateway: \"{}\"".format(me, err))
    sys.exit(6)

  okchk = (chk == wantchk)

  if(not okchk):
    # not sure that I need to exit if "chk" isn't what we wanted.
    sys.stderr.write("ERROR: {}: Incorrect checksum. Wanted '{}', got '{}'\n".format(me, wantchk, chk))
    #sys.exit(7)

  # make sure we got a good IP address
  receivedIP = "{}.{}.{}.{}".format(str(ip1), str(ip2), str(ip3), str(ip4))
  try:
    gatewayIP = str(ipaddress.ip_address(receivedIP))
  except ValueError as err:
    print("ERROR: {}: got an invalid IP address from the gateway:\n  \"{}\"".format(me, err))
    sys.exit(8)
  except NameError as err:
    print("ERROR: {}: received garbage from the gateway:\n  \"{}\"".format(me, err))
    sys.exit(9)
  except:
    print("ERROR: {}: Couldn't get an IP address for the gateway.".format(me, err))
    sys.exit(10)
  
  if(verbose):
    print("gatewayIP: '{}'".format(gatewayIP))
    print("gatewayPort: '{}'".format(gatewayPort))
    print("gatewayType: '{}'".format(gatewayType))
    print("gatewaySubtype: '{}'".format(gatewaySubtype))
    print("gatewayName: '{}'".format(gatewayName.decode("utf-8")))

  return gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk

if __name__ == "__main__":
  verbose = True
  gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk = findGateway(verbose)
