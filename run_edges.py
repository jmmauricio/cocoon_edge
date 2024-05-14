
import subprocess
import json
import multiprocessing

def run_command(host):
    host_pid = host['host_pid']
    emec_api_id = host['emec_api_id']

    command = f"sudo mnexec -a {host_pid} python3 ./edges/edge.py {emec_api_id} -cfg_dev ./emec_emu/pv_2_3_bess/config_devices.json -cfg_ctrl './emec_emu/pv_2_3_bess/config_controller.json'"
    print(command)
    subprocess.run(command, shell=True)

    


def run_in_host(json_file):
    # Read JSON data from file
    with open(json_file, "r") as fobj:
        hosts_dict = json.load(fobj)

    for item in hosts_dict:
        host_pid = hosts_dict[item]['pid']
        api_id = item
        host_dict = {'host_id':item, 'emec_api_id':api_id,'host_pid':host_pid}
        process = multiprocessing.Process(target=run_command, args=(host_dict,))
        process.start()
        
if __name__ == "__main__":

    run_in_host('./com_emu/hosts.json')

# dump = '''
# <Host POI: POI-eth0:10.0.0.3,POI-eth1:None pid=212899> 
# <Host PPC: PPC-eth0:10.0.0.4 pid=212901> 
# <Host Probe: Probe-eth0:10.0.0.5 pid=212903> 
# <Host h0101: h0101-eth0:10.0.1.1,h0101-eth1:None pid=212905> 
# <Host h0102: h0102-eth0:10.0.1.2,h0102-eth1:None pid=212907> 
# <OVSSwitch sPOI: lo:127.0.0.1,sPOI-eth1:None,sPOI-eth2:None,sPOI-eth3:None,sPOI-eth4:None pid=212884> 
# <OVSSwitch s0101: lo:127.0.0.1,s0101-eth1:None,s0101-eth2:None,s0101-eth3:None pid=212887> 
# <OVSSwitch s0102: lo:127.0.0.1,s0102-eth1:None,s0102-eth2:None pid=212890> 
# <OVSSwitch sEEMU: lo:127.0.0.1,enp0s8:None,sEEMU-eth2:None,sEEMU-eth3:None,sEEMU-eth4:None pid=212893> 
# <OVSController c0: 127.0.0.1:6633 pid=212876> 
# '''

# hosts = {'POI':{'api_id':'POI'},
#          'h0101':{'api_id':'LV0101'},
#          'h0102':{'api_id':'LV0102'},
#          }

# lines = dump.split('\n')

# for line in lines:
#     if 'Host' in line:
#         host_name = (line.split(':')[0].split(' ')[1])
#         host_pid = (line.split('pid=')[1][:-2])

#         if host_name in hosts:
        
#             hosts[host_name].update({'pid':host_pid})

# # h0003 python3 edge.py POI -cfg_dev config_devices.json & 
# # h0101 python3 edge.py LV0101 -cfg_dev config_devices.json &
# # h0102 python3 edge.py LV0102 -cfg_dev config_devices.json &


# # sudo mnexec -a 10125 bash

# for host in hosts:
#     host_pid = hosts[host]['pid']
#     api_id = hosts[host]['api_id']
#     print(f"sudo mnexec -a {host_pid} python3 edge.py {api_id} -cfg_dev config_devices.json")


