# constants
# mostly just protocol codes from https://github.com/ceisenach/screenlogic_over_ip

# copyright 2018, Keith P Jolley, keithpjolley@gmail.com, squalor heights, ca, usa
# Thu May 31 16:47:03 PDT 2018

import sys
import os
import struct

def me(): return(os.path.basename(sys.argv[0]))

# Protocol header for every (non-datagram) message sent to/from
# the gateway. 
# From Figure 1 of Section 3 of Protocol_Document.pdf from the above github url,
# this header describes the first 8 bytes:
# 0          2          4           8                              N
# | MSG CD 1 | MSG CD 2 | Data Size | Message Data (parameters) -> |
# 
class header:
  fmt    = "<HHI"
  length = struct.calcsize(fmt)

# Some of the message codes as documented in Sections 4 and 5 of the above PDF.
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
