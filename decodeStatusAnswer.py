# statusAnswer.py
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

# Don't look at me, i'm hideous.
# Decoding network structures is ugly and error prone.
# 

import struct
import numpy as np

# expects:
#   "want" is the type of data we are looking for
#     see https://docs.python.org/3/library/struct.html#format-characters
#     I make (un)educated guesses on if I think the data will be signed or unsigned.
#   "buff" is the buffer to extract from
#   "offset" is where in the buffer to read from
# returns (data, newoffset) where:
#  "data" is sizeof("want") byte(s) from "want" starting at "offset"
#  "newoffset" is "offset + sizeof("want") to help keep track of where in "buff" to read next
def getSome(want, buff, offset):
  fmt = "<" + want
  newoffset = offset + struct.calcsize(fmt)
  return struct.unpack_from(fmt, buff, offset)[0], newoffset

# decode the gateway's response to a "status" query
# see: https://github.com/parnic/node-screenlogic/blob/master/messages/SLPoolStatusMessage.js
def decodeStatusAnswer(data):
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

  # fast forward 3 bytes. why? because.
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

  # ok, this is enough. my brain hurts. if i was in charge i'd make every single one of these their
  # own pool message rather than have this monolithic datastructure. however, nobody asked me my 
  # opinion when they were designing this...

  # i'll add more decoding if i have a specific requirement for it. until then, cheers.
