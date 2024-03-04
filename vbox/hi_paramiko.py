
import paramiko, sys, getpass
import logging 
hostname = "127.0.0.2"
username = "ingelectus"
password = "ingelectus"
port = 2002
import time


# Create SSH client

nics = [
    {"interface_name": "enp2s0","ip":"10.0.0.10"},
    {"interface_name": "enp2s1","ip":"10.0.0.11"},
    {"interface_name": "enp2s2","ip":"10.0.0.12"},
    {"interface_name": "enp0s8","ip":"10.0.0.13"},    
    {"interface_name": "enp0s9","ip":"10.0.0.14"}, 
    {"interface_name":"enp0s10","ip":"10.0.0.15"},
    {"interface_name":"enp0s16","ip":"10.0.0.16"},
    {"interface_name":"enp0s17","ip":"10.0.0.17"},
    {"interface_name":"enp0s18","ip":"10.0.0.18"},
    {"interface_name":"enp0s19","ip":"10.0.0.19"} 
              ]
for nic in nics:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(nic['interface_name'])
    client.connect(hostname=hostname,port=port,username=username,password=password)
    stdin, stdout, stderr = client.exec_command(f"sudo -S /usr/sbin/ifconfig {nic['interface_name']} {nic['ip']}/24")
    stdin.write('ingelectus\n')
    print(stdout.readlines())

    client.close()

    time.sleep(0.1)

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

