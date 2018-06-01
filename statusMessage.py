# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import struct
import numpy as np

def getSome(want, data, offset):
  fmt = "<" + want
  newoffset = offset + struct.calcsize(fmt)
  return struct.unpack_from(fmt, data, offset)[0], newoffset

def decodeStatusMessage(data):
  ok, offset = getSome("I", data, 0)
  print("ok: {}".format(ok))

  freezeMode, offset = getSome("B", data, offset)
  print("freezeMode: {}".format(freezeMode))

  remotes, offset = getSome("B", data, offset)
  print("remotes: {}".format(remotes))

  poolDelay, offset = getSome("B", data, offset)
  print("poolDelay: {}".format(poolDelay))

  spaDelay, offset = getSome("B", data, offset)
  print("spaDelay: {}".format(spaDelay))

  cleanerDelay, offset = getSome("B", data, offset)
  print("cleanerDelay: {}".format(cleanerDelay))

  # skip 3 bytes
  offset = offset + struct.calcsize("3B")

  airTemp, offset = getSome("i", data, offset)
  print("airTemp: {}".format(airTemp))

  bodiesCount, offset = getSome("I", data, offset)
  bodiesCount = min(bodiesCount, 2)
  print("bodiesCount: {}".format(bodiesCount))
  
  currentTemp  = np.zeros(bodiesCount+1, dtype=int)
  heatStatus   = np.zeros(bodiesCount+1, dtype=int)
  setPoint     = np.zeros(bodiesCount+1, dtype=int)
  coolSetPoint = np.zeros(bodiesCount+1, dtype=int)
  heatMode     = np.zeros(bodiesCount+1, dtype=int)

  for i in range(bodiesCount):
    bodyType, offset = getSome("I", data, offset)
    if(bodyType not in range(2)): bodyType = 0

    currentTemp[bodyType], offset = getSome("i", data, offset)
    print("  currentTemp[{}]: {}".format(bodyType, currentTemp[bodyType]))

    heatStatus[bodyType], offset = getSome("i", data, offset)
    print("  heatStatus[{}]: {}".format(bodyType, heatStatus[bodyType]))

    setPoint[bodyType], offset = getSome("i", data, offset)
    print("  setPoint[{}]: {}".format(bodyType, setPoint[bodyType]))

    coolSetPoint[bodyType], offset = getSome("i", data, offset)
    print("  coolSetPoint[{}]: {}".format(bodyType, coolSetPoint[bodyType]))

    heatMode[bodyType], offset = getSome("i", data, offset)
    print("  heatMode[{}]: {}".format(bodyType, heatMode[bodyType]))
    print("")
  
  circuitCount, offset = getSome("I", data, offset)
  print("circuitCount: {}".format(circuitCount))

  heatMode = np.zeros(bodiesCount+1, dtype=int)
