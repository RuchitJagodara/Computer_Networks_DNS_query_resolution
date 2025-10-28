#!/usr/bin/python3
"""
CS331 Assignment 2: DNS Query Resolution Topology
THIS FILE IS CONFIGURED FOR PART C & D (Custom DNS Resolver)
"""

from mininet.net import Mininet
from mininet.node import Host, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def create_topology():
    """Creates and configures the DNS resolver topology."""

    net = Mininet(
        controller=None,  # No controller needed
        switch=OVSKernelSwitch,
        host=Host,
        link=TCLink
    )

    info('*** Adding Hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    dns = net.addHost('dns', ip='10.0.0.5/24') # Your custom resolver host

    info('*** Adding Switches\n')
    # Set failMode to 'standalone' to force L2 learning
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')
    s4 = net.addSwitch('s4', failMode='standalone')

    info('*** Adding NAT for internet connectivity\n')
    # connect=False disables the automatic link
    # Make sure to find your real internet-facing interface (e.g., 'eth0', 'enp0s3')
    # and add it if 'ping 8.8.8.8' fails for the 'dns' host.
    # Example: nat = net.addNAT(..., nat_iface='enp0s3')
    nat = net.addNAT(ip='10.0.0.254/24', inNamespace=False, connect=False)
    
    info('*** Adding Links (with BW and Delay)\n')
    # Manually link NAT to a switch
    net.addLink(nat, s1) 
    
    # Host-to-Switch links
    net.addLink(h1, s1, bw=100, delay='2ms')
    net.addLink(h2, s2, bw=100, delay='2ms')
    net.addLink(h3, s3, bw=100, delay='2ms')
    net.addLink(h4, s4, bw=100, delay='2ms')
    net.addLink(dns, s2, bw=100, delay='1ms')

    # Switch-to-Switch links
    net.addLink(s1, s2, bw=100, delay='5ms')
    net.addLink(s2, s3, bw=100, delay='8ms')
    net.addLink(s3, s4, bw=100, delay='10ms')

    info('*** Starting network\n')
    net.start()

    info('*** Setting default internet route for hosts\n')
    # Tell all hosts to use the NAT as their gateway
    for host in [h1, h2, h3, h4, dns]:
        host.cmd(f'ip route add default via 10.0.0.254')


    # --- Configuration for Part C & D ---
    # This section is now permanently active in this file
    
    info('*** Configuring Host DNS settings (for Part C)\n')
    for host in [h1, h2, h3, h4]:
        # Set the DNS server to our custom resolver
        host.cmd(f'echo "nameserver 10.0.0.5" > /etc/resolv.conf')
        info(f'Set DNS for {host.name} to 10.0.0.5\n')
    
    info('*** Starting Custom DNS Resolver on 10.0.0.5 (for Part D)\n')
    # This command runs your custom_resolver.py on the 'dns' host
    # We use 'sudo' to grant permission to bind to port 53.
    # Make sure your resolver filename (e.g., 'custom_resolver.py') is exact!
    dns.cmd('sudo python3 custom_resolver.py &')
    info('Resolver script initiated.\n')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()