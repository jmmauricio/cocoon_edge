
* cd to the cocoon_edge folder and run
* sudo python3 ./com_emu/pv_m_n_bess_mn.py

* Open new terminal and run:
* sudo python3 ./edges/run_edges.py

mininet> dump

<Host PPC: PPC-eth0:10.0.0.4,PPC-eth1:None pid=1098> 

* Open new terminal and run:
* cd ppc
* sudo mnexec -a 1119 bash
* python3 ppc_modbus.py

* run dashboard
