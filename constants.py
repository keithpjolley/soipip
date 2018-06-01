# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import sys
import os
import struct

def me(): return(os.path.basename(sys.argv[0]))

class header:
  fmt    = "<HHI"
  length = struct.calcsize(fmt)

class code:
  MSG_CODE_1        = 0
  UNKNOWN_ANSWER    = 13
  CHALLENGE_QUERY   = 14
  CHALLENGE_ANSWER  = CHALLENGE_QUERY  + 1
  LOCALLOGIN_QUERY  = 27
  LOCALLOGIN_ANSWER = LOCALLOGIN_QUERY + 1
  VERSION_QUERY     = 8120
  VERSION_ANSWER    = VERSION_QUERY    + 1
  POOLSTATUS_QUERY  = 12526
  POOLSTATUS_ANSWER = POOLSTATUS_QUERY + 1
