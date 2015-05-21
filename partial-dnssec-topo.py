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
        replaced_dirs = [ ('/var/log', '/home/mininet/partial-dnssec-deployment-setup/config/%(name)s/var/log'),
                          ('/etc/bind', '/home/mininet/partial-dnssec-deployment-setup/config/%(name)s/etc/bind')]
        
        linkconfig = {'bw': 10, 'delay': '1ms', 'loss': 0,
                      'max_queue_size': max_queue_size }

        self.nat_switch = self.addSwitch('s1')
        self.resolver = self.addHost('h1', privateDirs=replaced_dirs)
        self.localdns = self.addHost('h2', privateDirs=replaced_dirs)

        self.addLink(self.nat_switch, self.resolver, port1=1, **linkconfig)
        self.addLink(self.nat_switch, self.localdns, port1=2, **linkconfig)


    def start_bind(self):
        Node(self.resolver).cmd('service bind9 start')
        Node(self.localdns).cmd('service bind9 start')
        
        
if __name__ == '__main__':
    print "Entry"
    topo = partial_dnssec_topo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
    print "created topology"
    rootnode = connectToInternet(net, switch='s1')
    print "connectToInternet returned"
    net.topo.start_bind()

    CLI(net)
    stopNAT(rootnode)
    net.stop()
