# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

from constants import *
import findGateway
import struct

def makeMessageString(string):
  data = string.encode()
  length = len(data)
  pad = 4 - (length % 4)  # pad to multiple of 4 (i know i may pad when not needed. who cares)
  fmt = "<I" + str(length) + "s" + str(pad) + "x"
  return struct.pack(fmt, length, data)  # "x" is padding repeated 'pad' times

def getMessageString(data):
  length = len(data)
  size = struct.unpack_from("<I", data, 0)[0]
  return struct.unpack_from("<" + str(size) + "s", data, struct.calcsize("<I"))[0].decode("utf-8")

def makeMessage(msgCode2, messageData=b''):
  # if "msgCode1" is ever not zero, add it back into the parameters.
  # this pack works as expected even if messageData is empty
  return struct.pack(header.fmt + str(len(messageData)) + "s", code.MSG_CODE_1, msgCode2, len(messageData), messageData)

def decodeMessage(message):
  if not message:
    sys.stderr.write("WARNING: {}: no data to decodeMessage()\n".format(me))
    return
    
  messageBytes = len(message) - header.length
  rcvCode1, rcvCode2, rcvLen, data = struct.unpack(header.fmt + str(messageBytes) + "s", message)
  if(rcvLen != messageBytes):
    sys.stderr.write("WARNING: {}: rcvLen({}) != messageBytes({}).\n".format(me, rcvLen, messageBytes))
  if(rcvCode2 == code.UNKNOWN_ANSWER):
    sys.stderr.write("WARNING: {}: rcvCode2({}) != expectCode2({}).\n".format(me, rcvCode2, expectCode2))
  return rcvCode2, data # return raw data
