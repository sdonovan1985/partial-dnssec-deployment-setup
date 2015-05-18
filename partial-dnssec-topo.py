#!/usr/bin/python

from nat import *
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom
from mininet.node import RemoteController



class partial_dnssec_topo(Topo):
    def __init__(self, cpu=.1, max_queue_size=None, **params):
        ''' 
        Topology is simple. There are two hosts and one switch.
               Internet
                  |
              NAT switch
                |    |
            +---+    +---+
            |            |
        Resolver       Local DNS
    
        The NAT switch connects up to the Internet, and both hosts connect via
        the switch. Each host is the same *except* for config files for BIND.
        '''

        Topo.__init__(self, **params)
        # Thes two tuples are to use outside director
        resolver_dirs = [ ('/var/log', '/home/mininet/partial-dnssec-deployment-setup/config/%(name)s/var/log') ]
        localdns_dirs = [ ('/var/log', '/home/mininet/partial-dnssec-deployment-setup/config/%(name)s/var/log') ]
        
        linkconfig = {'bw': 10, 'delay': '1ms', 'loss': 0,
                      'max_queue_size': max_queue_size }

        nat_switch = self.addSwitch('s1')
        resolver = self.addHost('h1', privateDirs=resolver_dirs)
        localdns = self.addHost('h2', privateDirs=localdns_dirs)

        self.addLink(nat_switch, resolver, port1=1, **linkconfig)
        self.addLink(nat_switch, localdns, port1=2, **linkconfig)
        
        
if __name__ == '__main__':
    print "Entry"
    topo = partial_dnssec_topo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
    print "created topology"
    rootnode = connectToInternet(net, switch='s1')
    print "connectToInternet returned"

    CLI(net)
    stopNAT(rootnode)
    net.stop()
