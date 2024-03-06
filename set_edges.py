
import paramiko, sys, getpass
import logging 
import subprocess
import time

directory = '"C:\Program Files\Oracle\VirtualBox"'




#C:\Program Files\Oracle\VirtualBox\VBoxManage modifyvm "CIG-1" --natpf1 "ssh",tcp,127.0.0.10,,2010,22


def set_ssh_forwardings(data):

    vms = data["vms"]
    for item in vms:

        #"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "CIG-1" --natpf1 "guestssh,tcp,,127.0.0.10,2222,,22"

        edge_id   = item['name']
        ssh_ip    = item['ssh_ip']
        ssh_port  = item['ssh_port'] 

        print(f'ssh for {edge_id}')

        command = f'VBoxManage.exe modifyvm "{edge_id}" --natpf1 "ssh,tcp,{ssh_ip},{ssh_port},,22"'
        subprocess.run(f'cd /D {directory} && {command}', shell=True, check=True)

        time.sleep(0.2)

def set_ips(data,nic_ids):

    end_nodes = data['end_nodes']
    vms = data['vms']

    for item in end_nodes:

        username = "ingelectus"
        password = "ingelectus"


        edge_id = item['name']

        for vm in vms:
            if vm['name'] == item['vm_name']:
                ssh_ip = vm['ssh_ip']
                ssh_port  = vm['ssh_port'] 
                edge_name = item['name']

        adapter_number = item['adapter_number']
        adapter_name = nic_ids[adapter_number]

        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f'adapter_name = {adapter_name}')
        client.connect(hostname=ssh_ip,port=ssh_port,username=username,password=password)
        stdin, stdout, stderr = client.exec_command(f"sudo -S /usr/sbin/ifconfig {adapter_name} {item['modbus_ip']}/24")
        stdin.write('ingelectus\n')
        print(stdout.readlines())

        stdin, stdout, stderr = client.exec_command(f"sudo -S rm -r cocoon_edge")
        stdin.write('ingelectus\n')
        stdin, stdout, stderr = client.exec_command(f"git clone https://github.com/jmmauricio/cocoon_edge.git")
        print(stdout.readlines())

        # stdin, stdout, stderr = client.exec_command(f"cd cocoon_edge")
        # print(stdout.readlines())

        stdin, stdout, stderr = client.exec_command(f"cd cocoon_edge && nohup sudo -S python3 edge.py {edge_name}")
        stdin.write('ingelectus\n')        
        print(stdout.readlines())


        client.close()

        time.sleep(1)



if __name__ == "__main__":

    nics = [
             {"adapter_number": "enp0s8","modbus_ip":"10.0.0.10","modbus_port":502,"ssh_ip":"127.0.0.10","ssh_port":2010,"edge_id":"LV0101"},
             {"interface_name": "enp0s8","modbus_ip":"10.0.0.11","modbus_port":502,"ssh_ip":"127.0.0.11","ssh_port":2011,"edge_id":"CIG-2"}
        ]
    
    nic_ids = {0:'enp0s3',1:'enp0s8',2:'enp0s9',3:'enp0s10',
               4:'enp0s16',5:'enp0s17',6:'enp0s18',7:'enp0s19',
               8:'enp2s0',9:'enp2s1',10:'enp2s2',11:'enp2s3'}
    
    data = {
        "switches":[
            {"name":"SwPOI", "pos_x":0,"pos_y":0},
            {"name":"Sw0101","pos_x":-200,"pos_y":0},
            {"name":"Sw0102","pos_x":-350,"pos_y":0},
            {"name":"Sw0103","pos_x":-500,"pos_y":0},
            {"name":"Sw0104","pos_x":-650,"pos_y":0},
            {"name":"Sw0105","pos_x":-800,"pos_y":0}
        ],
        "end_nodes":[
            # {"name":"POI","modbus_ip":"10.0.0.2","modbus_port":502, "type":"vm", "vm_name":"POI","adapter_number":1,"pos_x": 110,"pos_y":-7},
            # {"name":"PPC","modbus_ip":"10.0.0.3","modbus_port":502, "type":"vm", "vm_name":"ppc","adapter_number":1,"pos_x": -50,"pos_y":-100},
             {"name":"LV0101","modbus_ip":"10.0.0.10","modbus_port":502, "type":"vm", "vm_name":"CIG01","adapter_number":1,"pos_x": -200,"pos_y":-150},
            {"name":"LV0102","modbus_ip":"10.0.0.11","modbus_port":502, "type":"vm", "vm_name":"CIG02","adapter_number":1,"pos_x": -350,"pos_y":-150},
            {"name":"LV0103","modbus_ip":"10.0.0.12","modbus_port":502, "type":"vm", "vm_name":"CIG03","adapter_number":1,"pos_x": -500,"pos_y":-150},
            {"name":"LV0104","modbus_ip":"10.0.0.13","modbus_port":502, "type":"vm", "vm_name":"CIG04","adapter_number":1,"pos_x": -650,"pos_y":-150},
            {"name":"LV0105","modbus_ip":"10.0.0.14","modbus_port":502, "type":"vm", "vm_name":"CIG05","adapter_number":1,"pos_x": -800,"pos_y":-150},
            {"name":"Probe", "ip":"10.0.0.4", "type":"vpcs","pos_x":0,"pos_y":200},
        ],
        "links":[
            {"node_j":"POI","adapter_number_j":1,"port_number_j":0,"node_k":"SwPOI","adapter_number_k":0,"port_number_k":0},
            {"node_j":"PPC","adapter_number_j":1,"port_number_j":0,"node_k":"SwPOI","adapter_number_k":0,"port_number_k":1},
            {"node_j":"LV0101","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0101","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0102","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0102","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0103","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0103","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0104","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0104","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0105","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0105","adapter_number_k":0,"port_number_k":0},
            {"node_j":"SwPOI", "adapter_number_j":0,"port_number_j":2,"node_k":"Sw0101","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0101","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0102","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0102","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0103","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0103","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0104","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0104","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0105","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Probe", "adapter_number_j":0,"port_number_j":0,"node_k":"SwPOI","adapter_number_k":0,"port_number_k":3}
        ],
        "vms":[
 #           {"name":"ppc",   "ssh_ip":"127.0.0.3", "ssh_port":2003},
            # {"name":"POI",   "ssh_ip":"127.0.0.2", "ssh_port":2002},
            {"name":"CIG01", "ssh_ip":"127.0.0.10", "ssh_port":2010},
            # {"name":"CIG02", "ssh_ip":"127.0.0.11", "ssh_port":2011},
            # {"name":"CIG03", "ssh_ip":"127.0.0.12", "ssh_port":2012},
            # {"name":"CIG04", "ssh_ip":"127.0.0.13", "ssh_port":2013},
            # {"name":"CIG05", "ssh_ip":"127.0.0.14", "ssh_port":2014}        
        ]
    }

    #set_ssh_forwardings(data)
    set_ips(data,nic_ids)


# try:
#     # Create SSH client
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Connect to the server
#     client.connect(hostname, port, username, password)

#     # Open a session
#     session = client.get_transport().open_session()

#     # Execute the reboot command
#     session.exec_command('sudo reboot')

# finally:
#     # Close the SSH client
#     client.close()



# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
# client.connect(hostname, port=2010, username=username, password=password)

# # stdin, stdout,stderr = client.exec_command("sudo -S -p ls")
# # client.write(f'ingelectus\n')
# # print(repr(stdout.read()))
# # client.flush()
# # client.close()

# command = "sudo -S -p ls"
# command = "sudo -S -p /usr/bin/python3 /home/ingelectus/hola.py"
# command = "/usr/bin/python3 /home/ingelectus/hola.py"
# command = "python3 hola.py"
# command = "ls"

# #logging.info("Job[%s]: Executing: %s" % ('hola', command))
# stdin, stdout, stderr = client.exec_command(command=command)
# #stdin.write(password + "\n")
# stdin.flush()
# stdoutput = [line for line in stdout]
# stderroutput = [line for line in stderr]

# print(stdoutput)

# client.close()
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
# client.connect(hostname, port="2010", username=username, password=password)
# for command in 'echo "Hello, world!"', 'uname', 'uptime':
#     stdin, stdout, stderr = client.exec_command(command)
#     stdin.close()
#     print(repr(stdout.read()))
#     stdout.close()
#     print(repr(stderr.read()))
#     stderr.close()
# client.close

# import paramiko

# command = "df"

# # Update the next three lines with your
# # server's information

# host = "127.0.0.10"
# port = 2010
# username = "ingelectus"
# password = "ingelectus"
# import paramiko


# # Command to execute (replace with your command)
# command = 'cd /home/ingelectus/workspace/cocoon_edge; ls; nohup sudo python3 edge.py LV0102 -autoip enp0s8 -apiip 192.168.56.1 &'
# command = 'python3 hola.py\n'

# _stdin, _stdout,_stderr = client.exec_command("python3 edge.py LV0101 -autoip enp0s8 -apiip 192.168.56.1")


# # SSH client setup
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# try:
#     # Connect to the server
#     client.connect(host, port, username, password)

#     # Execute the command
#     stdin, stdout, stderr = client.exec_command(command)

#     # Print command output
#     for line in stdout:
#         print(line.strip())

#     # Print any errors
#     for line in stderr:
#         print(line.strip())

# finally:
#     # Close the SSH client
#     client.close()



# # Print command output
# output = channel.recv(1).decode()
# print(output)



# #_stdin, _stdout,_stderr = ssh.exec_command("cd  /home/ingelectus/workspace/cocoon_edge; ls; python3 edge.py LV0102 -autoip enp0s8 -apiip 192.168.56.1")
# _stdin, _stdout,_stderr = ssh.exec_command("cd  /home/ingelectus/workspace/cocoon_edge; ls; sudo python3 edge.py LV0102 -autoip enp0s8 -apiip 192.168.56.1")
# _stdin.write('ingelectus' + "\n")

# print(_stdout.read().decode())

# # _stdin, _stdout,_stderr = client.exec_command("cd workspace/cocoon_edge; pwd")
# # print(_stdout.read().decode())

 


# # _stdin, _stdout,_stderr = client.exec_command("sudo python3 edge.py LV0101 -autoip enp0s8 -apiip 192.168.56.1")
# # print(_stdout.read().decode())

