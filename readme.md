
## Running localy

* Start emuplator.py at Host computer

In the VM Guest:

* cd to the cocoon_edge folder and run
* sudo python3 ./com_emu/pv_m_n_bess_mn.py
* sudo python3 ./com_emu/pv_m_n_bess_mn_vpn.py

* Open new terminal and run:
* sudo python3 ./edges/run_edges.py

mininet> dump

<Host PPC: PPC-eth0:10.0.0.4,PPC-eth1:None pid=1098> 

sudo mnexec -a 6919 bash 
sudo mnexec -a 6925 bash 


* Open new terminal and run:
* cd ppc
* sudo mnexec -a 1119 bash
* python3 ppc_modbus.py

* run dashboard

## Run VPN and test

sudo wg-quick up jmmauricio-lab
python3 -m http.server 8089
curl 10.0.0.10:8089

## Routing

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -I FORWARD -i enp0s8 -o jmmauricio-lab -j ACCEPT
sudo iptables -I FORWARD -i jmmauricio-lab -o enp0s8 -m state --state RELATED,ESTABLISHED -j ACCEPT

sudo mnexec -a 9481 bash


sudo brctl addif br1 jmmauricio-lab
sudo ip link set br1 up

## gRPC

python3 -m pip install grpcio-tools --break-system-packages