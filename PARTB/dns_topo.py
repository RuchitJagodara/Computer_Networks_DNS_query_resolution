#!/usr/bin/python3
"""
CS331 Assignment 2: DNS Query Resolution Topology
Author: [Your Name]
Date: [Current Date]
"""

from mininet.net import Mininet
from mininet.node import Host, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def create_topology():
    """Creates and configures the DNS resolver topology."""

    #
    # --- FIX 1: Set controller to None ---
    #
    net = Mininet(
        controller=None,  # No controller needed, switches will act as L2 hubs
        switch=OVSKernelSwitch,
        host=Host,
        link=TCLink
    )

    #
    # --- FIX 2: Comment out this line ---
    #
    # info('*** Adding Controller\n')
    # net.addController('c0')

    info('*** Adding Hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    dns = net.addHost('dns', ip='10.0.0.5/24') # Your custom resolver host

    info('*** Adding Switches\n')
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')
    s4 = net.addSwitch('s4', failMode='standalone')

    info('*** Adding NAT for internet connectivity\n')
    nat = net.addNAT(ip='10.0.0.254/24', inNamespace=False, connect=False)
    
    info('*** Adding Links (with BW and Delay)\n')
    net.addLink(nat, s1) 
    
    net.addLink(h1, s1, bw=100, delay='2ms')
    net.addLink(h2, s2, bw=100, delay='2ms')
    net.addLink(h3, s3, bw=100, delay='2ms')
    net.addLink(h4, s4, bw=100, delay='2ms')
    net.addLink(dns, s2, bw=100, delay='1ms')

    net.addLink(s1, s2, bw=100, delay='5ms')
    net.addLink(s2, s3, bw=100, delay='8ms')
    net.addLink(s3, s4, bw=100, delay='10ms')

    info('*** Starting network\n')
    net.start()

    info('*** Setting default internet route for hosts\n')
    for host in [h1, h2, h3, h4, dns]:
        host.cmd(f'ip route add default via 10.0.0.254')

    # --- Configuration for Part B ---
    info('*** Configuring hosts for Part B (public DNS)\n')
    for host in [h1, h2, h3, h4]:
        host.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')

    # --- Configuration for Part C & D (Keep commented out for now) ---
    # info('*** Configuring Host DNS settings (for Part C)\n')
    # ... (rest of Part C/D code) ...

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()