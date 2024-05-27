from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def myNetwork():
    net = Mininet(link=TCLink, switch=OVSSwitch)

    info('*** Adding hosts\n')
    h1 = net.addHost('h1')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')

    info('*** Creating links\n')
    net.addLink(h1, s1)

    info('*** Starting network\n')
    net.start()

    # Connect Mininet network to the VPN interface
    h1.cmd('ip route add default via 10.0.0.10 dev jmmauricio-lab')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
