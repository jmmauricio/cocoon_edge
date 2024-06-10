#!/usr/bin/env python3
'''
h0101 python3 linker.py LV0101 -cfg_dev config_devices.json
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
import numpy as np
from modbus import modbus_client

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)


class Linker:

    def __init__(self, cfg_dev, cfg_ctrl) -> None:
        # self.name = name
         
        with open(cfg_ctrl,'r') as fobj:
            self.config_controller = json.loads(fobj.read())

        with open(cfg_dev,'r') as fobj:
            self.config_devices = json.loads(fobj.read())


        self.linker_config = {}
        self.linker_config.update({'api_ip':self.config_devices['api']['host']})
        self.linker_config.update({'api_port':self.config_devices['api']['port']})

        # logging.info(self.linker_config)

        self.devices = []
  
        for device in self.config_devices['devices']:

            device_config = device['config']
            device.update(self.config_devices['configs'][device_config])

            for item in self.config_controller['configuration']['collector']['config']['devices']:
                if item['id'] ==  device['ing_id']:
                    adapterID = item["adapterID"]
                    device.update({"adapterID":adapterID})

            # read adapter configuration
            for item in self.config_controller['configuration']['collector']['config']['adapters']:
                if item['id'] ==  adapterID:
                    adapter = item

            to_device = device['to_device']

            for item in to_device:
                item.update(adapter['config'][item['ing_name']]) # get adapter_ID in config_controller.json
                emec_id = device['emec_id']
                emec_prefix = item['emec_prefix']
                item.update({'emec_name':f'{emec_prefix}_{emec_id}'})

                linker_reg_0 = device['linker_reg_0']
                linker_reg = item['linker_reg']
                item.update({'linkner_modbus_reg':linker_reg_0+linker_reg})


                

        #     # self.linker_config.update(item)
        #     # api_configs = config_devices['api_configs']
        #     # api_config = api_configs[item['api_config']]
        #     # self.linker_config.update({'api_config':api_config})
        #     #print('api_config', api_config)





        #     adapter_config = adapter['config']

        #     device.update({'to_device':[]})
        #     for to_device in self.config_devices['configs'][device['config']]['to_device']:
        #         print(to_device)

        #         ing_name = to_device['ing_name']
        #         to_device.update({'type':adapter_config[ing_name]['type']})
        #         to_device.update({'format':adapter_config[ing_name]['format']})
        #         emec_name = f"{to_device['emec_prefix']}_{device['emec_id']}"
        #         to_device.update({'emec_name':emec_name})
                
        #         K_emec2modbus = 1.0 
        #         if to_device['ing_name'] in  ['ActivePower','ReactivePower']:
        #             if device['ing_type'] == 'inverter':
        #                 for item in  self.config_controller['inverters']:
        #                     if device['ing_id'] == item['id']:
        #                         K_emec2modbus = item['sbase']     
        #         to_device.update({'K_emec2modbus':K_emec2modbus})  

        #         modbus_reg = device['linker_reg_0'] + to_device['linker_reg']

        #         to_device.update({'modbus_reg':modbus_reg})

        #         device['to_device'] += to_device

        #     for from_device in self.config_devices['configs'][device['config']]['from_device']:

        #         ing_name = from_device['ing_name']
        #         from_device.update({'type':adapter_config[ing_name]['type']})
        #         from_device.update({'format':adapter_config[ing_name]['format']})
        #         emec_name = f"{from_device['emec_prefix']}_{device['emec_id']}"
        #         from_device.update({'emec_name':emec_name})

    
            self.devices += [device]

        for device in self.devices:
            print(device)
            print('')

            # type = adapter_config[device['ing_name']]['type']


                    # api_id = device['api_id']
                    # linker_reg_0 = device['linker_reg_0']

                    # api_config = device['api_config']
                    # config = e.config_devices['api_configs'][api_config]

                    # for item in config['from_api']:
                    #     from_api = f"{item['api_prefix']}_{api_id}"
                    #     type = adapter_config[item['modbus_variable']]['type']
                    #     format = adapter_config[item['modbus_variable']]['format']
                    #     to_modbus = linker_reg_0 + item['linker_reg']




        #     # get adapter configuration
        #     for item in self.config_controller['configuration']['collector']['config']['adapters']:
        #         if item['id'] ==  device['adapterID']:
        #             device.update({"modbus_config":item['config']})

        #     # is the device an inverter?
        #     for item in self.config_controller['inverters']:
        #         if item['id'] ==  device['id']:    
        #             device.update({"inverter":item}) # if it is, get parameters.

        #     
        # #print(self.linker_config)

        self.modbus_ip = self.config_devices['linker']['host']
        self.modbus_port = self.config_devices['linker']['port']    


    # self.device = config_devices

    # # from_api and to_api dictionaries for devices initialization
    # if 'to_api' in self.device: 
    #     self.to_api = self.device['to_api']
    # else: self.to_api = []
    # if 'from_api' in self.device: 
    #     self.from_api = self.device['from_api']    
    # else: self.from_api = []

    def setup(self):
    
            self.modbus_client = modbus_client.Modbus_client(self.modbus_ip,self.modbus_port)

            self.api_client = http.client.HTTPConnection(self.linker_config['api_ip'], self.linker_config['api_port'])
            
            logging.info(f"Connected to Emulator API in ip = {self.linker_config['api_ip']}, port = {self.linker_config['api_port']}")

            self.api_headers = {'Content-type': 'application/json'}

    def update(self):

                    
        self.modbus_client.start()

        linker_config = self.linker_config
        while True:
#             # from modbus to api
#             to_api_dict = {}
#             for item in linker_config['api_config']['to_api']:
#                 modbus_variable = linker_config['modbus_config'][item['modbus_variable']]
#                 modbus_variable_id = item['modbus_variable']  
#                 K_api2modbus = 1.0 
#                 if modbus_variable_id in  ['SetActivePower','SetReactivePower']:
#                     if 'inverter' in linker_config:
#                         K_api2modbus = linker_config['inverter']['sbase']    

#                 api_prefix = item['api_prefix']
#                 api_var_name = f"{api_prefix}_{linker_config['api_id']}"
                
#                 # from modbus:
#                 mb_value = self.modbus_client.read(modbus_variable['address'], modbus_variable['type'],format=modbus_variable['format'])
#                 #print(f"{self.modbus_variable}@{self.modbus_ip}:{self.modbus_port},'->',{api_var_name}")

#                 # to api
#                 api_value = mb_value/K_api2modbus/modbus_variable['scale']
#                 to_api_dict.update({api_var_name:api_value})

#                 logging.debug(f"{modbus_variable_id}@{self.modbus_ip}:{self.modbus_port}/{modbus_variable['address']} -> {api_var_name} = {api_value}")           
                   
#             to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
#             self.api_client.request('POST', '/setpoints', to_api_json, self.api_headers)     # Send POST request
#             response = self.api_client.getresponse() # Get response from server
#             response_string = response.read().decode()     


            # from modbus to device
                
            self.api_client.request("GET", "/measures") # Send a GET request for the number
            response = self.api_client.getresponse() # Get the response from the server
            from_emec_measurements_dict = json.loads(response.read().decode()) # Read the response data

            
            for device in self.devices:
                
                for to_device in device['to_device']:
                    emec_name = to_device['emec_name']
                    emec_value = from_emec_measurements_dict[emec_name]
                    modbus_value = int(emec_value*to_device['K_emec2modbus'])
                    self.modbus_client.write(modbus_value,to_device['modbus_reg'], to_device['type'],format=to_device['format'])

                    print(emec_name, modbus_value,to_device['modbus_reg'], to_device['type'], to_device['format'])

                time.sleep(0.5)


                # # get adapter_ID in config_controller.json
                # for item in e.config_controller['configuration']['collector']['config']['adapters']:
                #     if item['id'] ==  device['api_config']:
                #         adapter = item
                
                # adapter_config = adapter['config']

                # api_id = device['api_id']
                # linker_reg_0 = device['linker_reg_0']

                # api_config = device['api_config']
                # config = e.config_devices['api_configs'][api_config]

                # for item in config['from_api']:
                #     from_api = f"{item['api_prefix']}_{api_id}"
                #     type = adapter_config[item['modbus_variable']]['type']
                #     format = adapter_config[item['modbus_variable']]['format']
                #     to_modbus = linker_reg_0 + item['linker_reg']

                #     K_emec2modbus = 1.0 
                #     if item['modbus_variable'] in  ['ActivePower','ReactivePower']:
                #         if 'inverter' in linker_config:
                #             K_api2modbus = linker_config['inverter']['sbase']                        

                #     value_emec = from_api_measurements_dict[from_api]
                #     value_mbus = value_emec*K_emec2modbus
                #     print(item['modbus_variable'])
                #     #print(from_api, value_emec, to_modbus, type, format, value_mbus)



#             for item in linker_config['api_config']['from_api']:
#                 modbus_variable = linker_config['modbus_config'][item['modbus_variable']]
#                 modbus_variable_id = item['modbus_variable']  
#                 K_api2modbus = 1.0 
#                 if modbus_variable_id in  ['ActivePower','ReactivePower']:
#                     if 'inverter' in linker_config:
#                         K_api2modbus = linker_config['inverter']['sbase']    

#                 api_prefix = item['api_prefix']
#                 api_var_name = f"{api_prefix}_{linker_config['api_id']}"

#                 # from api 
#                 value_api = from_api_measurements_dict[api_var_name]*K_api2modbus

#                 # to modbus:
#                 value_mb = int(modbus_variable['scale']*value_api)
#                 
#                 #print(f"{modbus_variable}@{modbus_ip}:{modbus_port},'->',api_var_name")
#                 logging.debug(f"{api_var_name} = {value_api} -> {modbus_variable_id}@{self.modbus_ip}:{self.modbus_port}/{modbus_variable['address']} = {value_mb}")           
#                 #print(f"{api_var_name} = {value_api} -> {modbus_variable_id}@{self.modbus_ip}:{self.modbus_port}/{modbus_variable['address']} = {value_mb}")
            


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
    logging.info(f'Starting server start at: {address}')
    server = StartTcpServer(context=context,address=address)    

def linker_run(cfg_dev, cfg_ctrl):

    e = Linker(cfg_dev, cfg_ctrl)
    e.setup()

    p_modbus_server = Process(target=modbus_server, args=(e.modbus_ip,e.modbus_port,))
    p_modbus_server.start()
    
    time.sleep(2)

    e.update()


if __name__ == "__main__":

    M = 1
    N = 2
    N_regs_dev = 32*4

    for m in range(M):
        for n in range(N):
            k = N_regs_dev*(m*N + n) + 1024

            # print(f'm = {m}, n = {n}, k = {k}')

    cfg_dev = "../emec_emu/pv_1_2_bess/config_devices.json"
    cfg_ctrl = "../emec_emu/pv_1_2_bess/config_controller.json"

    #linker_run(cfg_dev, cfg_ctrl)

    e = Linker(cfg_dev, cfg_ctrl)
    print(e.devices)

    # for device in e.config_devices['devices']:

    #     # get adapter_ID in config_controller.json
    #     for item in e.config_controller['configuration']['collector']['config']['adapters']:
    #         if item['id'] ==  device['api_config']:
    #             adapter = item
        
    #     adapter_config = adapter['config']

    #     api_id = device['api_id']
    #     linker_reg_0 = device['linker_reg_0']

    #     api_config = device['api_config']
    #     config = e.config_devices['api_configs'][api_config]

    #     for item in config['from_api']:
    #         from_api = f"{item['api_prefix']}_{api_id}"
    #         type = adapter_config[item['modbus_variable']]['type']
    #         format = adapter_config[item['modbus_variable']]['format']
    #         to_modbus = linker_reg_0 + item['linker_reg']
    #         print(from_api, to_modbus, type, format)


    # parser = argparse.ArgumentParser()
    # parser.add_argument("id", help="id name of the device")
    # parser.add_argument("-cfg_dev", help="config_devices.json file")
    # parser.add_argument("-cfg_ctrl", help="config_controller.json file")
    # args = parser.parse_args()
    # name = args.id    

    
    
    # if args.cfg_dev:
    #     cfg_dev = args.cfg_dev
    # else: 
    #     cfg_dev = "./emec_emu/config_devices.json"

    # if args.cfg_ctrl:
    #     cfg_ctrl = args.cfg_ctrl
    # else: 
    #     cfg_ctrl = "./emec_emu/config_controller.json"


    # linker_run(name, cfg_dev, cfg_ctrl)




#     parser = argparse.ArgumentParser()
#     parser.add_argument("id", help="id name of the device")
#     parser.add_argument("-autoip", help="id name of the device")
#     parser.add_argument("-apiip", help="id name of the device")
#     parser.add_argument("-cfgip", help="id name of the device")

#     args = parser.parse_args()
#     name = args.id

#     if args.autoip:
#         auto_config(name,args.autoip,args.apiip)
#     elif args.cfgip:
#         linker_config = api_config(name,args.cfgip)




               
#     time.sleep(1)
    
#     p_linker = Process(target=linker_run, args=(linker_config,))
#     p_linker.start()





#         # emulator api client
#         self.api_ip = self.device['emu_api_ip']
#         self.api_port = self.device['emu_api_port']
#         self.api_headers = {'Content-type': 'application/json'}

#         # modbus client
#         print(self.modbus_server_port)
#         self.modbus_client = ModbusTcpClient(self.modbus_server_ip, port=self.modbus_server_port)


#     def start(self):

#         self.modbus_client.connect()

#         uint16_min =       0
#         uint16_max =  65_535
        
#         modbus_min = uint16_min
#         modbus_max = uint16_max

#         for item in self.to_api:

#             api_min = item['api']['min']
#             api_max = item['api']['max']

#             val_api = item['api']['ini']
#             val_mb = int((val_api - api_min)*(modbus_max - modbus_min)/(api_max - api_min) + modbus_min)
#             val_mb = np.clip(val_mb,0,65535)
#             self.modbus_client.write_register(item['modbus']['reg_number'], val_mb)

#         self.update_thread = Thread(target = self.update)
#         self.update_thread.start()

#     def update(self):

#         self.api_client = http.client.HTTPConnection(self.api_ip, self.api_port)

#         while True:

#             int32_min = -2_147_483_648 
#             int32_max =  2_147_483_647
#             uint16_min =       0
#             uint16_max =  65_535

#             modbus_min = uint16_min
#             modbus_max = uint16_max


#             # from api to modbus 
#             self.api_client.request("GET", "/measures") # Send a GET request for the number
#             response = self.api_client.getresponse() # Get the response from the server
#             from_api_measurements_dict = json.loads(response.read().decode()) # Read the response data

#             self.from_api_dict = {}
#             # (val_api - api_min)/(api_max - api_min)  = (val_mb - modbus_min)/(modbus_max - modbus_min)
#             for item in self.from_api:

#                 api_min = item['api']['min']
#                 api_max = item['api']['max']

#                 val_api = from_api_measurements_dict[item['api']['name']]
#                 self.from_api_dict.update({item['api']['name']:val_api})
#                 val_mb = int((val_api - api_min)*(modbus_max - modbus_min)/(api_max - api_min) + modbus_min)
#                 self.modbus_client.write_register(item['modbus']['reg_number'], val_mb)

#             print(self.from_api_dict)
#             time.sleep(0.05)


#             # from modbus to api 
#             modbus_response = self.modbus_client.read_holding_registers(0, 10)
#             to_api_dict = {}
#             for item in self.to_api:
#                 api_min = item['api']['min']
#                 api_max = item['api']['max']
#                 val_mb = modbus_response.registers[item['modbus']['reg_number']]
#                 val_api = (val_mb - modbus_min)/(modbus_max - modbus_min)*(api_max - api_min)  + api_min
#                 to_api_dict.update({item['api']['name']:val_api})
            
#             to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
#             self.api_client.request('POST', '/setpoints', to_api_json, self.api_headers)     # Send POST request
#             response = self.api_client.getresponse() # Get response from server
#             response_string = response.read().decode()            
#             time.sleep(0.05)

# def linker_run(linker_config):

#     e = linker(linker_config)
#     e.start()

# def modbus_server(name):

#     # read configuration file 
#     with open('config_devices.json','r') as fobj:
#         config_devices = json.loads(fobj.read())

#     # find current device in configuration
#     for item in config_devices['devices']:
#         if item['id'] ==  name:
#             device = item

#     # modbus server
#     modbus_server_ip   = device['modbus_ip']
#     modbus_server_port = device['modbus_port']

#     # Define your Modbus data blocks
#     store = ModbusSlaveContext(
#         di=ModbusSequentialDataBlock(0, [0]*100),   # Discrete Inputs
#         co=ModbusSequentialDataBlock(0, [0]*100),   # Coils
#         hr=ModbusSequentialDataBlock(0, [0]*100),   # Holding Registers
#         ir=ModbusSequentialDataBlock(0, [0]*100)    # Input Registers
#     )
#     context = ModbusServerContext(slaves=store, single=True)

#     address = (modbus_server_ip, modbus_server_port)
#     print(f'Server start at: {address}')
#     server = StartTcpServer(context=context,address=address)
    
# def auto_config(name,adapter_name,api_ip):

#     gen_id = name
#     MM = int(name[-4:-2])
#     NN = int(name[-2:])
    
#     ip = MM*10 + NN-1
#     modbus_ip = f"10.0.0.{ip}" 

#     netmask = "255.255.255.0"  # Change this to your desired netmask
    
#     configure(adapter_name, modbus_ip, netmask)

#     # read configuration file 
#     with open('config_devices_template.json','r') as fobj:
#         config_devices = fobj.read()

#     config_devices = config_devices.replace('{api_ip}',api_ip)
#     config_devices = config_devices.replace('{modbus_ip}',modbus_ip)
#     config_devices = config_devices.replace('{gen_id}',gen_id)
#     config_devices = config_devices.replace('{modbus_port}','502')
    

#     # read configuration file 
#     with open('config_devices.json','w') as fobj:
#         fobj.write(config_devices)

# def api_config(name,config_api_ip):

#     api_ip = config_api_ip
#     api_port = 8001
#     api_headers = {'Content-type': 'application/json'}

#     api_client = http.client.HTTPConnection(api_ip, api_port)
#     to_api_json = json.dumps({"name":name})
#     api_client.request("GET", "/config_linker",to_api_json,api_headers) 
#     response = api_client.getresponse() # Get the response from the server
#     return json.loads(response.read().decode()) # Read the response data



        
# if __name__ == "__main__":


# #
    

#         # # read configuration file 
#         # with open('config_devices.json','r') as fobj:
#         #     self.config_devices = json.loads(fobj.read())

#         # # find current device in configuration
#         # for item in self.config_devices['devices']:
#         #     if item['id'] ==  name:
#         #         self.device = item