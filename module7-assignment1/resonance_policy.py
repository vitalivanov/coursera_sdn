'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 7 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz

Created by: Vitaliy Ivanov
'''

################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.examples.load_balancer import *

class ResonancePolicy():

  state_policy_map = {}

  def __init__(self):
    self.state_policy_map['default'] = self.default_policy

  def get_policy(self, state):
    if self.state_policy_map.has_key(state):
      return self.state_policy_map[state]
    else:
      return self.default_policy

  """ Default state policy """
  def default_policy(self):
    return drop

class LBPolicy(ResonancePolicy):
  def __init__(self, fsm):
    self.fsm = fsm

  def portA_policy(self):
    public_ip = IP('10.0.0.100')
    client_ips = [IP('10.0.0.1')]
    repeating_R =  [IP('10.0.0.2')]
    # This will replace the incoming packet[src=10.0.0.1, dst=10.0.0.100] to packet[src=10.0.0.1, dst=10.0.0.2] and
    #                            and packet[src=10.0.0.1, dst=10.0.0.2] back to packet[src=10.0.0.1, dst=10.0.0.100]
    return rewrite(zip(client_ips, repeating_R), public_ip)

  def portB_policy(self):
    public_ip = IP('10.0.0.100')
    client_ips = [IP('10.0.0.1')]
    repeating_R =  [IP('10.0.0.3')]
    # This will replace the incoming packet[src=10.0.0.1, dst=10.0.0.100] to packet[src=10.0.0.1, dst=10.0.0.3] and
    #                            and packet[src=10.0.0.1, dst=10.0.0.3] back to packet[src=10.0.0.1, dst=10.0.0.100]
    return rewrite(zip(client_ips, repeating_R), public_ip)

# --------- Update the code below ------------

  def default_policy(self):
    # Add the logic to return the right policy (i.e., portA_policy or portB_policy
    # based on the state of the FSMs)

    #hint:
    # 1. get the list of hosts in portA state
    portA_hosts = self.fsm.get_portA_hosts()
    print "port A hosts: " + str(portA_hosts)
    # 2. match the incoming packet's source and destination ip against that list of hosts
    # (using pyretic predicates i.e., "match", "modify", and "if_" etc)
    # 3. if there is a match apply portA policy else apply portB policy
    return if_(parallel([match(srcip=IP(host)) for host in portA_hosts])+parallel([match(dstip=IP(host)) for host in portA_hosts]), self.portA_policy(), self.portB_policy())
