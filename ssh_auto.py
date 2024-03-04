#from virtualbox.library import VBoxException
from virtualbox.library import VirtualBoxManager

def add_port_forwarding_rule(vm_name_or_id, adapter_name_or_id, rule_name, protocol, host_ip, host_port, guest_ip, guest_port):
    # Initialize VirtualBox Manager
    mgr = VirtualBoxManager(None, None)

    # Get VirtualBox object
    vbox = mgr.vbox

    # Find the VM by name or ID
    vm = vbox.find_machine(vm_name_or_id)

    # Get the settings of the VM
    settings = vm.get_settings()

    # Find the network adapter by name or ID
    adapter = settings.find_network_adapter_by_name_or_id(adapter_name_or_id)

    # Add a port forwarding rule to the adapter
    try:
        adapter.create_nat_rule(rule_name, protocol, host_ip, host_port, guest_ip, guest_port)
    except VBoxException as e:
        print(f"Failed to add port forwarding rule: {e}")
        return

    # Apply the changes to the VM
    vm.save_settings()

    print(f"Port forwarding rule '{rule_name}' added to network adapter '{adapter_name_or_id}' of VM '{vm_name_or_id}'.")

if __name__ == "__main__":
    # Replace the values with your VM and port forwarding rule details
    add_port_forwarding_rule(
        vm_name_or_id='Your_VM_Name_or_ID',
        adapter_name_or_id='Name_or_ID_of_Network_Adapter',
        rule_name='ssh',
        protocol='TCP',  # 'TCP' or 'UDP'
        host_ip='127.0.0.10',      # Leave empty for all interfaces
        host_port='2010',
        guest_ip='',     # Leave empty for guest localhost
        guest_port='22'
    )
