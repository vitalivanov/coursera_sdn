'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz

Created by: Vitaliy Ivanov
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3:edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        # Add your logic here ...

        # Incoming params
        self.fanout = fanout
        self.linkopts1 = linkopts1
        self.linkopts2 = linkopts2
        self.linkopts3 = linkopts3

        # Numbering:  c1, a1..aN, e1..eN, h1..N
        self.coreNum = 1
        self.aggregationNum = 1
        self.edgeNum = 1
        self.hostNum = 1
        depth = 3
        # Build topology
        self.addTree(depth, fanout)

    def addTree(self, depth, fanout):
        """Add a subtree starting with node n.
           returns: last node added"""
        isCore = depth == 3
        isAggregation = depth == 2
        isEdge = depth == 1
        isHost = depth == 0

        if depth > 0:
            linkopts = dict()
            if isCore:
                node = self.addSwitch('c%s' % self.coreNum)
                self.coreNum += 1
                linkopts = self.linkopts1
            if isAggregation:
                node = self.addSwitch('a%s' % self.aggregationNum)
                self.aggregationNum += 1
                linkopts = self.linkopts2
            if isEdge:
                node = self.addSwitch('e%s' % self.edgeNum)
                self.edgeNum += 1
                linkopts = self.linkopts3
            for _ in range(fanout):
                child = self.addTree(depth - 1, fanout)
                self.addLink(node, child, **linkopts)
        else:
            node = self.addHost('h%s' % self.hostNum)
            self.hostNum += 1
        return node

def perfTest():
    "Create network and run simple performance test"
    linkopts1 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    linkopts2 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    linkopts3 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)
    net = Mininet(topo=topo, 
                 host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.stop()

# TODO: Used for tests. Uncomment to test locally.
#if __name__ == '__main__':
#    setLogLevel('info')
#    perfTest()

# TODO: Uncomment before submit
topos = { 'custom': ( lambda: CustomTopo() ) }
