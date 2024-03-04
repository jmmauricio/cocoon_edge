from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
import time


class Modbus_client:

    def __init__(self,ip,port) -> None:
        
        self.ip = ip
        self.port = port



    def start(self):

        self.modbus_client = ModbusTcpClient(self.ip, port=self.port)

    def close(self):

        self.modbus_client.close()

    def write_int32(self,value, reg_number, format = 'CDAB'):
        # write INT32
        if format == 'CDAB':
            builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

        builder.add_32bit_int(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_int32(self,reg_number, format = 'CDAB'):
        # read INT32
        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 2)
        if format == 'CDAB':
            decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        value = decoder.decode_32bit_int()
        return value

    def write_int16(self,value, reg_number, format = 'AB'):
        # write INT32
        if format == 'AB':
            builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

        builder.add_16bit_int(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_int16(self,reg_number, format = 'AB'):
        # read INT32
        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 2)
        if format == 'AB':
            decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        value = decoder.decode_16bit_int()
        return value

    def write_uint16(self,value, reg_number, format = 'AB'):
        # write INT32
        if format == 'AB':
            builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

        builder.add_16bit_uint(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_uint16(self,reg_number, format = 'AB'):
        # read INT32
        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 2)
        if format == 'AB':
            decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        value = decoder.decode_16bit_uint()
        return value

if __name__ == "__main__":

    ip = "192.168.0.10"
    port = 580

    mb = Modbus_client(ip,port=port)
    mb.start()

    print('Client started')

    value = 1_500_000
    reg_number = 97
    mb.write_int32(value, reg_number, format = 'CDAB')

    value_echo = mb.read_int32(reg_number, format = 'CDAB')
    print(value_echo)

    

