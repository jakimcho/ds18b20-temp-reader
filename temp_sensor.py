#! /usr/bin/env python

import transmit_msg
import ds18b20
from pprint import pprint
 
messages = ds18b20.read_temp()
pprint(messages)
if len(messages) > 0:
    res = transmit_msg.send(messages)
    print ("message sent to mongo" + str(res))
