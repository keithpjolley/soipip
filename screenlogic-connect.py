#! /usr/bin/env python
# -*- coding: UTF8 -*-
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import findGateway
import doQuery

if __name__ == "__main__":
  verbose = False
  gatewayIP, gatewayPort, gatewayType, gatewaySubtype, gatewayName, okchk = findGateway.findGateway(verbose)
  doQuery.queryGateway(gatewayIP, gatewayPort)
