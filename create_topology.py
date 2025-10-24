#!/usr/bin/python3

"""
CS331 Assignment 2: Custom Topology Script
"""

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class AssignmentTopo(Topo):
    """
    Custom Topology for CS331 Assignment 2
    """
    def build(self):
        # Add Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        dns_resolver = self.addHost('dns', ip='10.0.0.5/24')

        # Add Switches
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, stp=True)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, stp=True)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch, stp=True)
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch, stp=True)

        # Add Links with specified BW and Delay
        # Host to Switch links [cite: 16, 17, 19, 22]
        self.addLink(h1, s1, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h2, s2, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h3, s3, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h4, s4, cls=TCLink, bw=100, delay='2ms')
        
        # DNS Resolver to Switch link [cite: 30]
        self.addLink(dns_resolver, s2, cls=TCLink, bw=100, delay='1ms')

        # Switch to Switch links [cite: 24, 26, 28]
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='5ms')
        self.addLink(s2, s3, cls=TCLink, bw=100, delay='8ms')
        self.addLink(s3, s4, cls=TCLink, bw=100, delay='10ms')

def runNet():
    "Bootstrap and run the network"
    topo = AssignmentTopo()
    net = Mininet(
        topo=topo,
        link=TCLink,
        switch=OVSKernelSwitch,
        autoSetMacs=True,
        autoStaticArp=True
    )

    net.start()
    print("**********************************************")
    print("* Network is up. Run 'pingall' to test.      *")
    print("* Type 'exit' to quit.                       *")
    print("**********************************************")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    runNet()