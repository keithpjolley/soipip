#! /usr/bin/env python
# -*- coding: UTF8 -*-
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import sys
import socket
import struct
import ipaddress

def findGateway(verbose):
  bcast = "255.255.255.255"
  port  = 1444
  wantchk = 2
  addressfamily = socket.AF_INET
  data  = struct.pack('<bbbbbbbb', 1,0,0,0, 0,0,0,0)
  # Create a UDP socket
  try:
    udpSock = socket.socket(addressfamily, socket.SOCK_DGRAM)
  except:
    sys.stderr.write("ERROR: {}: socket.socket boarked.\n".format(me))
    sys.exit(1)
  try:
    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  except:
    sys.stderr.write("ERROR: {}: udpSock.setsockopt boarked.\n".format(me))
    sys.exit(2)
  if(verbose):
    print("Broadcasting for pentair systems...")
  try:
    udpSock.sendto(data, (bcast, port))
  except:
    sys.stderr.write("ERROR: {}: udpSock.sendto boarked.\n".format(me))
    sys.exit(3)
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
    sys.stderr.write("ERROR: {}: udpSock.close boarked.\n".format(me))
    sys.exit(5)
  system, port = server
  expectedfmt = "<I4BH2B"  # from one documentation source. must be a previous version...
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
    print("gatewayIP: {}".format(gatewayIP))
    print("gatewayPort: {}".format(gatewayPort))
    print("gatewayType: {}".format(gatewayType))
    print("gatewaySubtype: {}".format(gatewaySubtype))
    print("gatewayName: {}".format(gatewayName.decode("utf-8")))

  return gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk

if __name__ == "__main__":
  verbose = False
  gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk = findGateway(verbose)
  print("gatewayIP: {}".format(gatewayIP))
  print("gatewayPort: {}".format(gatewayPort))
