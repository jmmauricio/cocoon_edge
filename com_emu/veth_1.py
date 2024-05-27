from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

def myNetwork():
    net = Mininet(controller=OVSController, link=TCLink, switch=OVSSwitch)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')

    info('*** Adding host\n')
    h1 = net.addHost('h1', ip='10.0.0.3/24')

    info('*** Creating links\n')
    net.addLink(h1, s1)

    info('*** Adding interface veth1 to switch s1\n')
    _intf = Intf('veth1', node=s1)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
