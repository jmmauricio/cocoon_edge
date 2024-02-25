import subprocess

def configure(adapter_name, ip_address, netmask):
    try:
        # Bring down the network adapter
        subprocess.run(['sudo', 'ifconfig', adapter_name, 'down'], check=True)

        # Configure IP address and netmask
        subprocess.run(['sudo', 'ifconfig', adapter_name, ip_address, 'netmask', netmask], check=True)

        # Bring up the network adapter
        subprocess.run(['sudo', 'ifconfig', adapter_name, 'up'], check=True)

        print(f"Network adapter {adapter_name} configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    adapter_name = "enp0s8"  # Change this to your network adapter name
    ip_address = "10.0.0.10"  # Change this to your desired IP address
    netmask = "255.255.255.0"  # Change this to your desired netmask
    
    configure_network_adapter(adapter_name, ip_address, netmask)
