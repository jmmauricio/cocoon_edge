
import time
from pymodbus.client import ModbusTcpClient
import json
import numpy as np

class Device:

    def __init__(self,name) -> None:
        
        # read configuration file 
        with open('config_devices.json','r') as fobj:
            self.config_devices = json.loads(fobj.read())

        # find current device in configuration
        for item in self.config_devices['devices']:
            if item['id'] ==  name:
                self.device = item

        modbus_server_ip   = self.device['modbus_ip'] 
        modbus_server_port = self.device['modbus_port']   
        self.modbus_client = ModbusTcpClient(modbus_server_ip, port=modbus_server_port)
        self.modbus_client.connect() 

        self.uint16_min =       0
        self.uint16_max =  65_535

        self.modbus_min = self.uint16_min
        self.modbus_max = self.uint16_max

    def ini_set_q(self):

        self.S_nom = 1e3*self.device['S_mva']

        for setpoint in self.device['to_api']:
            if setpoint['api']['name'] == self.device['q_ref_name']:
                self.reg_number_q = setpoint['modbus']['reg_number']
                self.api_min_q = setpoint['api']['min']
                self.api_max_q = setpoint['api']['max']

    def set_q(self,q_pu):
        val_api = q_pu
        api_min = self.api_min_q
        api_max = self.api_max_q
        modbus_min = self.modbus_min
        modbus_max = self.modbus_max
        val_mb = int((val_api - api_min)*(modbus_max - modbus_min)/(api_max - api_min) + modbus_min)  
        val_mb = np.clip(val_mb,modbus_min,modbus_max)             
        self.modbus_client.write_register(self.reg_number_q,val_mb)

    def get_v(self):
        api_min = self.api_min_v
        api_max = self.api_max_v
        modbus_min = self.modbus_min
        modbus_max = self.modbus_max
        val_mb = self.modbus_client.read_holding_registers(0, 10).registers[self.reg_number_v]
        val_api = (val_mb - modbus_min)/(modbus_max - modbus_min)*(api_max - api_min)  + api_min                

        return  val_api       
  
    def ini_get_v(self):

        for measurement in self.device['from_api']:
            if measurement['api']['name'] == self.device['v_name']:
                self.reg_number_v = measurement['modbus']['reg_number']
                self.api_min_v = measurement['api']['min']
                self.api_max_v = measurement['api']['max']

