'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 7 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

import socket
import sys
import struct
import json
from optparse import OptionParser


CTRL_ADDR = '127.0.0.1'
CONN_PORT = 50001

eventTypes = {'lb': 0}

def main():

    desc = ( 'Send JSON Events' )
    usage = ( '%prog [options]\n'
              '(type %prog -h for details)' )
    op = OptionParser( description=desc, usage=usage )
    op.add_option( '--host-IP', '-i', action="store", 
                     dest="hostIP", help = 'the host IP for which a state change happens'  )

    op.add_option( '--event-type', '-e', type='choice',
                   dest="eventType",
                     choices=['lb'], 
                     help = '|'.join( ['lb'] )  )

    op.add_option( '--event-value', '-V', action="store", 
                     dest="eventValue", help = 'the host IP for which a state change happens'  )

    options, args = op.parse_args()
    eventnum = eventTypes[options.eventType]


    print options.hostIP

    data = dict(event=dict(event_id=1,      \
                           event_type=eventnum,    \
                           event_code=1,    \
                           description=1,   \
                           sender=dict(sender_id=1,   \
                                       description=1, \
                                       ip_addr=1,     \
                                       mac_addr=1),    \
                           data=dict(data_type=eventnum,     \
                                     data=options.hostIP,          \
                                     value=options.eventValue),         \
                           transition=dict(prev=1,    \
                                           next=1)    \
                           ))

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    s.connect((CTRL_ADDR, CONN_PORT))


    bufsize = len(data)

    # send data
    totalsent = 0
    s.send(json.dumps(data))
    s.close()

### START ###
if __name__ == '__main__':
    main()
### end of function ###
