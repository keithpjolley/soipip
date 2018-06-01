# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import struct
import doMessages
from constants import *

# login message
def createLoginMessage():
  # these constants are only for this message. keep them here.
  schema = 348
  connectionType = 0
  clientVersion = doMessages.makeMessageString(me())
  pid  = 2
  password = "mypasswd"
  passwd = doMessages.makeMessageString(password) # passwd must be <= 16 chars. empty is A-OK.
  fmt = "<II" + str(len(clientVersion)) + "s" + str(len(passwd)) + "sxI"
  return struct.pack(fmt, schema, connectionType, clientVersion, passwd, pid)
