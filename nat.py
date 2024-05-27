from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

def myNetwork():
    net = Mininet(link=TCLink)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    info('*** Adding NAT router\n')
    nat = net.addHost('nat0', cls=Node, ip='10.0.0.254/24')
    nat.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Creating links\n')
    net.addLink(h1, nat)
    net.addLink(h2, nat)

    # Attach the NAT router to the veth1 interface
    info('*** Attaching NAT to veth1\n')
    _intf = Intf('veth1', node=nat)
    nat.setIP('0.0.0.0', intf='veth1')

    info('*** Starting network\n')
    net.start()

    info('*** Configuring NAT\n')
    nat.cmd('dhclient veth1')  # Obtain IP address from DHCP on the bridged network
    nat.cmd('iptables -t nat -A POSTROUTING -o veth1 -j MASQUERADE')
    nat.cmd('iptables -A FORWARD -i veth1 -o nat0-eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    nat.cmd('iptables -A FORWARD -i nat0-eth0 -o veth1 -j ACCEPT')

    info('*** Running DHCP server on nat\n')
    nat.cmd('dnsmasq --interface=nat0-eth0 --dhcp-range=10.0.0.100,10.0.0.200,12h')

    # Set DNS server for Mininet hosts
    h1.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
    h2.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')

    h1.cmd('dhclient h1-eth0')
    h2.cmd('dhclient h2-eth0')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
