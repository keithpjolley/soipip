# doMessages.py
# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

# implements creating and reading pool messages

from constants import *
import struct

# Strings within messages are described at the start of Section 4 in Protocol_Document.pdf
# Send this function a string and it returns a properly encoded struct.
def makeMessageString(string):
  data = string.encode()
  length = len(data)
  pad = 4 - (length % 4)  # pad to multiple of 4 (i know i may pad when not needed. who cares)
  fmt = "<I" + str(length) + "s" + str(pad) + "x"
  return struct.pack(fmt, length, data)  # "x" is padding repeated 'pad' times

# send this function an encoded string and it returns "string"
def getMessageString(data):
  length = len(data)
  size = struct.unpack_from("<I", data, 0)[0]
  return struct.unpack_from("<" + str(size) + "s", data, struct.calcsize("<I"))[0].decode("utf-8")

# appends a header to an optional already formatted message.
# returns a complete pool message ready to send to the gateway.
def makeMessage(msgCode2, messageData=b''):
  # if "msgCode1" is ever not zero, add it back into the parameters.
  # this pack works as expected even if messageData is empty
  return struct.pack(header.fmt + str(len(messageData)) + "s", code.MSG_CODE_1, msgCode2, len(messageData), messageData)

# takes the header off of the pool message and returns just the message part
# contrary to its name it doesn't actually decode the message.
# decoding the message is ugly. i mean really ugly.
# this code warns, but doesn't do more than that, if it notices that the message
# length doesn't match what it advertises its length should be and also if
# the "message code 2" is "UNKNOWN."
# 
# send decodeMessage the raw pool message from the gateway and it returns a struct of
# the (message code, message)
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
