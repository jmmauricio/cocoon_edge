
import subprocess

#subprocess.run('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "CIG-1" --natpf1 "guestssh,tcp,,127.0.0.10,2222,,22"', check=True)
#subprocess.run(r'cd  ..', check=True)
#subprocess.run("dir", check=True)
directory = '"C:\Program Files\Oracle\VirtualBox"'
command = 'VBoxManage.exe modifyvm "CIG-1" --natpf1 "guestssh,tcp,127.0.0.10,2222,,22"'
subprocess.run(f'cd /D {directory} && {command}', shell=True, check=True)


# # Command to run (replace with your command)
# command = "ping"

# # Arguments for the command (replace with your arguments)
# arguments = ["-n", "4", "google.com"]

# # Run the command with arguments
# try:
#     # Use subprocess.run() for Python 3.5+
    
# except subprocess.CalledProcessError as e:
# import virtualbox
# import time
# vbox = virtualbox.VirtualBox()
# print([m.name for m in vbox.machines])


# session = virtualbox.Session()
# machine = vbox.find_machine("CIG-1")
# adapter = machine.get_network_adapter(0)
# print(adapter.set_property("guestssh,tcp,,127.0.0.10,2222,,22"))
#machine.attach_device
#adapter = machine.get_network_adapter('1')
# # progress = machine.launch_vm_process(session, "gui", "")
# # For virtualbox API 6_1 and above (VirtualBox 6.1.2+), use the following:
# progress = machine.launch_vm_process(session, "gui", [])
# progress.wait_for_completion()

# time.sleep(15)

#session.console.keyboard.put_keys("Hello, world!")
#guest_session = session.console.guest.create_session("ingelectus", "ingelectus")
# guest_session.directory_exists("C:\\Windows")

# proc, stdout, stderr = guest_session.execute("C:\\\\Windows\\System32\\cmd.exe", ["/C", "tasklist"])
# print(stdout)
