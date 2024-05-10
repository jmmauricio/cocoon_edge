'''
Two isolated networks three hosts are connected to both.
One host is only connected to the netwoek with domain 192.168.X.X

sudo fuser -k 6653/tcp
sudo mn -c
sudo python3 pv_mn_bess_mn.py

h00001 python3 emulator.py &

h0101 curl http://192.168.2.1:8000/measures

h0003 python3 edge.py POI -cfg_dev config_devices.json &
h0101 python3 edge.py LV0101 -cfg_dev config_devices.json &
h0102 python3 edge.py LV0102 -cfg_dev config_devices.json &


h0001 python3 ./modbus/modbus_client.py

sudo mnexec -a 1443 bash
sudo mnexec -a 1433 bash

sudo mnexec -a 1437 bash
sudo mnexec -a 1439 bash
'''



#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import time 

def interSecureModelNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='1.0.0.0/8')
    
    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=OVSController,
                      protocol='tcp',
                      port=6633)

    switchType = OVSKernelSwitch; 

    info( '*** Starting networking devices\n')
    sPOI =  net.addSwitch( 'sPOI', cls=switchType, dpid='1',failMode='standalone')    
    s0101 = net.addSwitch('s0101', cls=switchType, dpid='2',failMode='standalone')    
    s0102 = net.addSwitch('s0102', cls=switchType, dpid='3',failMode='standalone')    
    

    info( '*** Starting external connection\n')    
    sEEMU = net.addSwitch('sEEMU', cls=switchType, dpid='4',failMode='standalone')  # switch for the electrical emulator
    Intf( 'enp0s8', node=sEEMU )  # EDIT the interface name here! 

    info( '*** Starting hosts \n')
    POI   = net.addHost(  'POI', cls=Host, ip='10.0.0.3/16', defaultRoute='10.0.0.1',mac='00:00:00:00:00:03')  # POI 
    PPC   = net.addHost(  'PPC', cls=Host, ip='10.0.0.4/16', defaultRoute='10.0.0.1',mac='00:00:00:00:00:04')  # PPC
    Probe = net.addHost('Probe', cls=Host, ip='10.0.0.5/16', defaultRoute='10.0.0.1',mac='00:00:00:00:00:05')  # Probe    
    h0101 = net.addHost('h0101', cls=Host, ip='10.0.1.1/16', defaultRoute='10.0.0.1',mac='00:00:00:00:01:01')  # Gen 0101    
    h0102 = net.addHost('h0102', cls=Host, ip='10.0.1.2/16', defaultRoute='10.0.0.1',mac='00:00:00:00:01:02')  # Gen 0102    

    info( '*** Setting link parameters\n')
    #WAN1 = {'bw':1000,'delay':'20ms','loss':1,'jitter':'10ms'} 
    #GBPS = {'delay':'18ms'} 
    #MBPS = {'bw':10} 

    info( '*** Adding links\n')

    net.addLink(  POI, sPOI)
    net.addLink(  PPC, sPOI)
    net.addLink(Probe, sPOI)

    net.addLink( sPOI, s0101)
    net.addLink(s0101, s0102)

    net.addLink(h0101, s0101)
    net.addLink(h0102, s0102)

    net.addLink(  POI, sEEMU)
    net.addLink(h0101, sEEMU)
    net.addLink(h0102, sEEMU)

    #net.addLink(WANR1, DSS1GW, cls=TCLink , **MBPS)
    info( '\n')

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting networking devices \n')
    net.get( 'sPOI').start([])
    net.get('s0101').start([])
    net.get('s0102').start([])
    net.get('sEEMU').start([])
    info( '\n')

    info( '*** Preparing custom sgsim scripts \n')
    #CLI.do_webserver = webserver    
    net.get(  'POI').cmd('ifconfig POI-eth1 172.16.0.3 netmask 255.0.0.0')
    net.get(  'PPC').cmd('ifconfig PPC-eth1 172.16.0.4 netmask 255.0.0.0')
    #net.get('Probe').cmd('ifconfig Probe-eth1 10.0.0.5 netmask 255.0.0.0')
    net.get('h0101').cmd('ifconfig h0101-eth1 172.16.1.1 netmask 255.0.0.0')
    net.get('h0102').cmd('ifconfig h0102-eth1 172.16.1.2 netmask 255.0.0.0')
    info( '*** Model Started *** \n' )
    CLI(net)
    net.stop()

# def webserver(self, line):
#     "Starts Python Simple HTTP Server on h0101" 
#     net = self.mn   
#     info('Starting the webserver... \n')        
#     net.get('h0101').cmdPrint('xterm -geometry 90x30+10+10 -fa "Monospace" -fs 12 -T "Webserver" -e "python3 -m http.server 8080;bash"&') 
#     time.sleep(0.5)
   
if __name__ == '__main__':
    setLogLevel( 'info' )
    interSecureModelNetwork()





# from mininet.net import Mininet
# from mininet.topo import Topo
# from mininet.node import RemoteController
# from mininet.cli import CLI
# from mininet.link import Intf
# import time

# def build():

#     net = Mininet(topo=None, build=False, waitConnected=True )
#     # Add switches
#     s1 = net.addSwitch('s1')
#     s2 = net.addSwitch('s2')

#     net.addController(name='c1', node=s1)
#     net.addController(name='c2', node=s2)

#     # Add hosts to the first network
#     hPOI = net.addHost('h0001', ip='10.0.0.1/16')
#     hPPC = net.addHost('h0003', ip='10.0.0.3/16')
#     h0101 = net.addHost('h0101', ip='10.0.1.1/16')
#     h0102 = net.addHost('h0102', ip='10.0.1.2/16')

#     hPROB1 = net.addHost( 'h0005', ip='10.0.0.5/16')
#     hEMEC =  net.addHost('h00001', ip='192.168.2.1/16')

#     # h14 = net.get( 'h14' )
#     # h14.setIP('192.168.1.4')

#     #nat = net.addNAT(node=net.get( 's2' ), ip='192.168.1.6/24')
#     #nat = net.addNAT(node=net.get( 's2' ))


#     #Intf( 'enp0s8', node=net.get( 's2' ) )

#     # Connect hosts to switches
#     net.addLink(  hPOI, s1)
#     net.addLink(  hPPC, s1)
#     net.addLink( h0101, s1)
#     net.addLink( h0102, s1)
#     net.addLink(hPROB1, s1)

#     net.addLink( hPOI, s2, params1={ 'ip' : '192.168.0.1/16' })
#     net.addLink(h0101, s2, params1={ 'ip' : '192.168.1.1/16' })
#     net.addLink(h0102, s2, params1={ 'ip' : '192.168.1.2/16' })
#     net.addLink(hEMEC, s2)



#     return net
 

#     # Connect switches
#     #self.addLink(s1, s2)

# def create_network():
#     net = build()   
#     net.start()
#     net.pingAll()  # Optional: Test connectivity between hosts
#     print('Network started')

#     # hPOI = net.get('h0001')
#     # hPPC = net.get('h0003')
#     # h0101 = net.get('h0101')
#     # h0102 = net.get('h0102')

#     # hPROB1 = net.get( 'h0005')
#     # hEMEC =  net.get('h00001')

#     # hEMEC.sendCmd('python3 emulator.py &')
#     # time.sleep(10)
#     # print('Emulator started')

#     # hPOI.sendCmd('python3 edge.py POI -cfg_dev config_devices.json &')
#     # time.sleep(2)
#     # # hPOI.cmd('curl http://192.168.2.1:8000/measures')
#     # # hPOI.cmd('curl http://192.168.2.1:8000/measures')
#     # print('POI started')

#     # h0101.sendCmd('python3 edge.py LV0101 -cfg_dev config_devices.json &')
#     # time.sleep(2)
#     # # h0101.cmd('curl http://192.168.2.1:8000/measures')
#     # # h0101.cmd('curl http://192.168.2.1:8000/measures')
#     # print('Gen 0101')

#     # h0102.sendCmd('python3 edge.py LV0102 -cfg_dev config_devices.json &')
#     # time.sleep(2)
#     # # h0102.cmd('curl http://192.168.2.1:8000/measures')
#     # # h0102.cmd('curl http://192.168.2.1:8000/measures')
#     # print('Gen 0102')

    
#     #net.pingAll()  # Optional: Test connectivity between hosts
#     CLI(net)
#     net.stop()

# if __name__ == '__main__':
#     create_network()
