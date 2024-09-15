#!/usr/bin/env python3
'''
python ./edges/edge_modbus.py LINKER lmah -cfg_dev ./emec_emu/pv_1_2_bess/config_devices.json
python ./edges/edge_modbus.py L0101 dmlm -cfg_dev ./emec_emu/pv_1_2_bess/config_devices.json


This module can be run attached to a Mininet HOST emulating a device.

The module launch a MODBUS server where registers are configured as defined in the following files:

- config.json
- config_control.json 
- config_devices.json 

This server can be accessed  from the devices connected to the "real" Mininet network.

The module has also two clients, the client-com and the client-emec with the following objectives:

- client-com: it read and write the registers at the previous server
- client-emec: it reads and write registers of the linker server



h0101 python3 edge.py LV0101 -cfg_dev config_devices.json
python ./edges/edge_modbus.py LV0101 -cfg_dev ./emec_emu/pv_2_3_bess/config_controller.json


'''
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
import copy
import numpy as np
from modbus import modbus_client

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)


class Edge:

    def __init__(self, name, cfg_dev, cfg_ctrl) -> None:
        self.name = name
         
        with open(cfg_ctrl,'r') as fobj:
            self.config_controller = json.loads(fobj.read())

        with open(cfg_dev,'r') as fobj:
            self.config_devices = json.loads(fobj.read())

        self.edge_config = {}
        self.edge_config.update({'api_ip':self.config_devices['api']['host']})
        self.edge_config.update({'api_port':self.config_devices['api']['port']})

        self.modbus_linker_ip = self.config_devices['linker']['ip']
        self.modbus_linker_port = self.config_devices['linker']['port']

        logging.info(self.edge_config)


    def setup_device(self):
        
        print(self.name)
        # find current device in configuration file config_devices.json
        for item in self.config_devices['devices']:
            if item['emec_id'] == self.name:
                self.device_data = item
                break

        print(item)

        self.edge_config.update(item)
        self.config = self.config_devices['configs'][self.device_data['config']]
        self.setpoints_list = self.config['setpoints']
        self.measurements_list = self.config['measurements']
        self.modbus_ip = item['modbus_ip']
        self.modbus_port = item['modbus_port']

        # get adapter_ID in config_controller.json
        for item in self.config_controller['configuration']['collector']['config']['devices']:
            if item['id'] ==  self.edge_config['ing_id']:
                self.adapterID = item["adapterID"]
                break

        for item in self.config_controller["configuration"]["collector"]["config"]["adapters"]:
            if item['id'] == self.adapterID:
                self.adapter = item
                break

        for item in self.setpoints_list:
            item.update(self.adapter['config'][item['ing_name']])
            emec_name = f"{item['emec_prefix']}_{self.device_data['emec_id']}"
            item.update({'emec_name':emec_name})
            linker_reg = self.device_data['linker_reg_0'] + item['linker_reg']
            item.update({'linker_register':linker_reg})

        for item in self.measurements_list:
            item.update(self.adapter['config'][item['ing_name']])
            emec_name = f"{item['emec_prefix']}_{self.device_data['emec_id']}"
            item.update({'emec_name':emec_name})
            linker_reg = self.device_data['linker_reg_0'] + item['linker_reg']
            item.update({'linker_register':linker_reg})
    
    def setup_multiple_device(self):

        self.devices_list = []
            
        # find current device in configuration file config_devices.json
        for item in self.config_devices['devices']:
            self.name = item['emec_id']
            print(self.name)
            self.setup_device()
            print([(self.setpoints_list.copy(),self.measurements_list.copy())])
            self.devices_list += [(copy.deepcopy(self.setpoints_list),copy.deepcopy(self.measurements_list))]

        print(self.devices_list)

    def update_dmah(self):
        '''
        Device_MODBUS <-> API_http
        '''

        self.modbus_device_client = modbus_client.Modbus_client(self.modbus_ip,self.modbus_port)
        logging.info(f"Connected to device at ip = {self.modbus_ip}, port = {self.modbus_port}")
        self.modbus_device_client.start()  

        self.api_client = http.client.HTTPConnection(self.edge_config['api_ip'], self.edge_config['api_port'])
        logging.info(f"Connected to Emulator API in ip = {self.edge_config['api_ip']}, port = {self.edge_config['api_port']}")
        self.api_headers = {'Content-type': 'application/json'}


        while True:

            # Setpoints  ###############################################################################################
            
            emec_setpoints_dict = {}

            # read setpoints from modbus (real system side)
            for setpoint in self.setpoints_list:

                modbus_value = self.modbus_device_client.read(setpoint['address'], setpoint['type'],format=setpoint['format'])
                emec_value = modbus_value*setpoint['emec_scale']
                emec_setpoints_dict.update({setpoint['emec_name']:emec_value})
                print(f"modbus_value@{setpoint['address']} = {modbus_value}  -> {setpoint['emec_name']} = {emec_value}  ")

            # write setpoints in the emec emulator server
            setpoints_json = json.dumps(emec_setpoints_dict)  # Convert dictionary to JSON format
            self.api_client.request('POST', '/setpoints', setpoints_json, self.api_headers)     # Send POST request
            response = self.api_client.getresponse() # Get response from server
            response_string = response.read().decode()     

            # Measurements #####################################################################################

            # read measurements from emec emulator server
            self.api_client.request("GET", "/measures") # Send a GET request for the number
            response = self.api_client.getresponse() # Get the response from the server
            measurements_dict = json.loads(response.read().decode()) # Read the response data

            # write measurements in modbus (real system side)
            for meas in self.measurements_list:

                emec_value = measurements_dict[meas['emec_name']]
                modbus_value = int(emec_value/meas['emec_scale'])
                self.modbus_device_client.write(modbus_value, meas['address'], meas['type'],format=meas['format'])
                
                print(f"{meas['emec_name']} = {emec_value} -> modbus_value@{meas['address']} = {modbus_value}")


            # Emulator control #####################################################################################
            response = self.modbus_device_client.modbus_client.read_coils(0,1) 
            if response.bits[0]:
                break
            time.sleep(0.5)

    def update_dmlm(self):
        '''
        Device_MODBUS <-> Linker_MODBUS
        '''

        self.modbus_device_client = modbus_client.Modbus_client(self.modbus_ip,self.modbus_port)
        logging.info(f"Connected to device at ip = {self.modbus_ip}, port = {self.modbus_port}")
        self.modbus_device_client.start()  

        self.modbus_linker_client = modbus_client.Modbus_client(self.modbus_linker_ip,self.modbus_linker_port)
        logging.info(f"Connected to linker at ip = {self.modbus_linker_ip}, port = {self.modbus_linker_port}")
        self.modbus_linker_client.start()
                       
        while True:

            # Setpoints  ###############################################################################################
            
            # read setpoints from modbus (real system side)
            for setpoint in self.setpoints_list:

                modbus_value = self.modbus_device_client.read(setpoint['address'], setpoint['type'],format=setpoint['format'])
                self.modbus_linker_client.write(modbus_value, setpoint['linker_register'], setpoint['type'],format=setpoint['format']) 
                logging.info(f"device: {setpoint['emec_name']}@{self.modbus_ip}:{self.modbus_port}/{setpoint['address']} = {modbus_value} -> linker: {setpoint['emec_name']}@{self.modbus_linker_ip}:{self.modbus_linker_port}/{setpoint['linker_register']}")

            # Measurements #####################################################################################

            # write measurements in modbus (real system side)
            for meas in self.measurements_list:

                linker_value = self.modbus_linker_client.read(meas['linker_register'], meas['type'],format=meas['format'])
                self.modbus_device_client.write(linker_value, meas['linker_register'], meas['type'],format=meas['format'])

                #print(f"{meas['emec_name']} = {emec_value} -> modbus_value@{meas['address']} = {modbus_value}")


            # Emulator control #####################################################################################
            response = self.modbus_linker_client.modbus_client.read_coils(0,1) 
            if response.bits[0]:
                break
            time.sleep(0.5)

    def update_lmah(self):
        '''
        Linker_MODBUS - API_http
        '''

        self.modbus_linker_client = modbus_client.Modbus_client(self.modbus_linker_ip,self.modbus_linker_port)
        logging.info(f"Connected to linker at ip = {self.modbus_linker_ip}, port = {self.modbus_linker_port}")
        self.modbus_linker_client.start()        

        self.api_client = http.client.HTTPConnection(self.edge_config['api_ip'], self.edge_config['api_port'])
        logging.info(f"Connected to Emulator API at ip = {self.edge_config['api_ip']}, port = {self.edge_config['api_port']}")
        self.api_headers = {'Content-type': 'application/json'}

        while True:

            for setpoints_list,measurements_list in self.devices_list:

                # Setpoints  ###############################################################################################
                
                emec_setpoints_dict = {}

                # read setpoints from modbus (real system side)
                for setpoint in setpoints_list:

                    modbus_value = self.modbus_linker_client.read(setpoint['linker_register'], setpoint['type'],format=setpoint['format'])
                    emec_value = modbus_value*setpoint['emec_scale']
                    emec_setpoints_dict.update({setpoint['emec_name']:emec_value})
                    print(f"modbus_value@{setpoint['linker_register']} = {modbus_value}  -> {setpoint['emec_name']} = {emec_value}  ")

                # write setpoints in the emec emulator server
                setpoints_json = json.dumps(emec_setpoints_dict)  # Convert dictionary to JSON format
                self.api_client.request('POST', '/setpoints', setpoints_json, self.api_headers)     # Send POST request
                response = self.api_client.getresponse() # Get response from server
                response_string = response.read().decode()     


                # Measurements #####################################################################################

                # read measurements from emec emulator server
                self.api_client.request("GET", "/measures") # Send a GET request for the number
                response = self.api_client.getresponse() # Get the response from the server
                measurements_dict = json.loads(response.read().decode()) # Read the response data

                # write measurements in modbus (real system side)
                for meas in measurements_list:

                    emec_value = measurements_dict[meas['emec_name']]
                    modbus_value = int(emec_value/meas['emec_scale'])
                    self.modbus_linker_client.write(modbus_value, meas['linker_register'], meas['type'],format=meas['format'])
                    
                    print(f"{meas['emec_name']} = {emec_value} -> modbus_value@{meas['linker_register']} = {modbus_value}")


            # Emulator control #####################################################################################
            response = self.modbus_linker_client.modbus_client.read_coils(0,1) 
            if response.bits[0]:
                break
            time.sleep(0.5)


def modbus_server(modbus_server_ip,modbus_server_port):

    # Define your Modbus data blocks
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100000),   # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0]*100000),   # Coils
        hr=ModbusSequentialDataBlock(0, [0]*100000),   # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*100000)    # Input Registers
    )
    context = ModbusServerContext(slaves=store, single=True)

    address = (modbus_server_ip, modbus_server_port)
    logging.info(f'Starting modbus server at: {address}')
    server = StartTcpServer(context=context,address=address)    


def edge_run(name, mode,cfg_dev, cfg_ctrl):

    e = Edge(name, cfg_dev, cfg_ctrl)
    print(mode)

    if mode == 'dmah': # Device_MODBUS <-> API_http
        e.setup_device()
        p_modbus_server = Process(target=modbus_server, args=(e.modbus_ip,e.modbus_port,))
        print(f'Listening at {e.modbus_ip}, port {e.modbus_port}')
        p_modbus_server.start()
        time.sleep(1)
        e.update_dmah()

    if mode == 'dmlm': # Device_MODBUS <-> Linker_MODBUS
        e.setup_device()
        p_modbus_server = Process(target=modbus_server, args=(e.modbus_ip,e.modbus_port,))
        p_modbus_server.start()
        time.sleep(1)
        e.update_dmlm()
                
    if mode == 'lmah': # Linker_MODBUS <-> API_http
        e.setup_multiple_device()
        p_modbus_server = Process(target=modbus_server, args=(e.modbus_linker_ip,e.modbus_linker_port,))
        print(f'Listening at {e.modbus_linker_ip}, port {e.modbus_linker_port}')
        p_modbus_server.start()
        time.sleep(1)
        e.update_lmah()
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="id name of the device")
    parser.add_argument("mode", help="working mode")
    parser.add_argument("-cfg_dev", help="config_devices.json file")
    parser.add_argument("-cfg_ctrl", help="config_controller.json file")
    args = parser.parse_args()
    name = args.id    
    mode = args.mode
    
    if args.cfg_dev:
        cfg_dev = args.cfg_dev
    else: 
        cfg_dev = "./emec_emu/config_devices.json"

    if args.cfg_ctrl:
        cfg_ctrl = args.cfg_ctrl
    else: 
        cfg_ctrl = "./emec_emu/config_controller.json"

    edge_run(name, mode, cfg_dev, cfg_ctrl)
