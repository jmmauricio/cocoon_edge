#!/usr/bin/env python3
import argparse
import logging
from multiprocessing import Process
from pymodbus.client import ModbusTcpClient
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from threading import Thread
import json
import http.client
import time
from cocoon_edge.configure_nadapter import configure
import numpy as np

class Edge:

    def __init__(self,name) -> None:
        
        # read configuration file 
        with open('config_devices.json','r') as fobj:
            self.config_devices = json.loads(fobj.read())

        # find current device in configuration
        for item in self.config_devices['devices']:
            if item['id'] ==  name:
                self.device = item

        # from_api and to_api dictionaries for devices initialization
        if 'to_api' in self.device: 
            self.to_api = self.device['to_api']
        else: self.to_api = []
        if 'from_api' in self.device: 
            self.from_api = self.device['from_api']    
        else: self.from_api = []

        # modbus server
        self.modbus_server_ip   = self.device['modbus_ip']
        self.modbus_server_port = self.device['modbus_port']

        # emulator api client
        self.api_ip = self.config_devices['api']['host']
        self.api_port = self.config_devices['api']['port']
        self.api_headers = {'Content-type': 'application/json'}

        # modbus client
        print(self.modbus_server_port)
        self.modbus_client = ModbusTcpClient(self.modbus_server_ip, port=self.modbus_server_port)


    def start(self):

        self.modbus_client.connect()

        uint16_min =       0
        uint16_max =  65_535
        
        modbus_min = uint16_min
        modbus_max = uint16_max

        for item in self.to_api:

            api_min = item['api']['min']
            api_max = item['api']['max']

            val_api = item['api']['ini']
            val_mb = int((val_api - api_min)*(modbus_max - modbus_min)/(api_max - api_min) + modbus_min)
            val_mb = np.clip(val_mb,0,65535)
            self.modbus_client.write_register(item['modbus']['reg_number'], val_mb)

        self.update_thread = Thread(target = self.update)
        self.update_thread.start()

    def update(self):

        self.api_client = http.client.HTTPConnection(self.api_ip, self.api_port)

        while True:

            int32_min = -2_147_483_648 
            int32_max =  2_147_483_647
            uint16_min =       0
            uint16_max =  65_535

            modbus_min = uint16_min
            modbus_max = uint16_max


            # from api to modbus 
            self.api_client.request("GET", "/measures") # Send a GET request for the number
            response = self.api_client.getresponse() # Get the response from the server
            from_api_measurements_dict = json.loads(response.read().decode()) # Read the response data

            self.from_api_dict = {}
            # (val_api - api_min)/(api_max - api_min)  = (val_mb - modbus_min)/(modbus_max - modbus_min)
            for item in self.from_api:

                api_min = item['api']['min']
                api_max = item['api']['max']

                val_api = from_api_measurements_dict[item['api']['name']]
                self.from_api_dict.update({item['api']['name']:val_api})
                val_mb = int((val_api - api_min)*(modbus_max - modbus_min)/(api_max - api_min) + modbus_min)
                self.modbus_client.write_register(item['modbus']['reg_number'], val_mb)

            print(self.from_api_dict)
            time.sleep(0.05)


            # from modbus to api 
            modbus_response = self.modbus_client.read_holding_registers(0, 10)
            to_api_dict = {}
            for item in self.to_api:
                api_min = item['api']['min']
                api_max = item['api']['max']
                val_mb = modbus_response.registers[item['modbus']['reg_number']]
                val_api = (val_mb - modbus_min)/(modbus_max - modbus_min)*(api_max - api_min)  + api_min
                to_api_dict.update({item['api']['name']:val_api})
            
            to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
            self.api_client.request('POST', '/setpoints', to_api_json, self.api_headers)     # Send POST request
            response = self.api_client.getresponse() # Get response from server
            response_string = response.read().decode()            
            time.sleep(0.05)

def edge_run(name):

    e = Edge(name)
    e.start()

def modbus_server(name):

    # read configuration file 
    with open('config_devices.json','r') as fobj:
        config_devices = json.loads(fobj.read())

    # find current device in configuration
    for item in config_devices['devices']:
        if item['id'] ==  name:
            device = item

    # modbus server
    modbus_server_ip   = device['modbus_ip']
    modbus_server_port = device['modbus_port']

    # Define your Modbus data blocks
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),   # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0]*100),   # Coils
        hr=ModbusSequentialDataBlock(0, [0]*100),   # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*100)    # Input Registers
    )
    context = ModbusServerContext(slaves=store, single=True)

    address = (modbus_server_ip, modbus_server_port)
    print(f'Server start at: {address}')
    server = StartTcpServer(context=context,address=address)
    
def auto_config(name,adapter_name,api_ip):

    gen_id = name
    MM = int(name[-4:-2])
    NN = int(name[-2:])
    
    ip = MM*10 + NN-1
    modbus_ip = f"10.0.0.{ip}" 

    netmask = "255.255.255.0"  # Change this to your desired netmask
    
    configure(adapter_name, modbus_ip, netmask)

    # read configuration file 
    with open('config_devices_template.json','r') as fobj:
        config_devices = fobj.read()

    config_devices = config_devices.replace('{api_ip}',api_ip)
    config_devices = config_devices.replace('{modbus_ip}',modbus_ip)
    config_devices = config_devices.replace('{gen_id}',gen_id)
    config_devices = config_devices.replace('{modbus_port}','502')
    

    # read configuration file 
    with open('config_devices.json','w') as fobj:
        fobj.write(config_devices)

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="id name of the device")
    parser.add_argument("-autoip", help="id name of the device")
    parser.add_argument("-apiip", help="id name of the device")

    args = parser.parse_args()
    name = args.id

    if args.autoip:
        auto_config(name,args.autoip,args.apiip)

    p_modbus_server = Process(target=modbus_server, args=(name,))
    p_modbus_server.start()
               
    time.sleep(1)
    
    p_edge = Process(target=edge_run, args=(name,))
    p_edge.start()
#