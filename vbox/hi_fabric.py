from fabric import Connection

# SSH connection settings
host = '127.0.0.10'
user = 'ingelectus'
#key_filename = '/path/to/your/private/key.pem'  # if using SSH key authentication
password = 'ingelectus'  # if using password authentication

# Path to the Python script on the remote host
remote_script_path = 'hola.py'

# Define a function to execute the script
def execute_script(connection):
    # Run the Python script
    connection.run(f'python3 {remote_script_path}')
    #connection.run(f'ls')


    # Establish an SSH connection
with Connection(host=host, port=2010, user=user, connect_kwargs={ "password": password}) as conn:
       # with conn.cd('/home/ingelectus/workspace'):
        # Run the Python script within the specified directory
        #result = conn.sudo(f'python3 edge.py LV0102 -autoip enp0s8 -apiip 192.168.56.1')
        conn.sudo(f'sudo cd /home/ingelectus/workspace && ls', password='ingelectus')
        # Print the output of the command
        #print(result.stdout)

    #conn.run('python3 /home/ingelectus/workspace/cocoon_edge/edge.py LV0102 -autoip enp0s8 -apiip 192.168.56.1')
    

