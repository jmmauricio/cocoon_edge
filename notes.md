Inside Mininet-VM:

curl http://172.18.119.65:8000/measures

This IP is from:

    Wireless LAN adapter Wi-Fi:

    Connection-specific DNS Suffix  . : localdomain
    Link-local IPv6 Address . . . . . : fe80::ecf0:b6cd:10f:3cdf%17
    IPv4 Address. . . . . . . . . . . : 172.18.119.65
    Subnet Mask . . . . . . . . . . . : 255.255.0.0
    Default Gateway . . . . . . . . . : 172.18.1.1


Mininet-VM is configured with two network adapters

- Adapter 1: NAT
- Adapter 2: Bridge

Bridge configured as:

    $ sudo ifconfig eth1 down
    $ sudo ifconfig 192.168.0.91
    $ sudo ifconfig eth1 up
