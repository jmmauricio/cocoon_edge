from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
import time

try: 
    dummy = Endian.Little
except:
    Endian.Little = Endian.LITTLE
    Endian.Big = Endian.BIG


class Modbus_client:

    def __init__(self,ip,port) -> None:
        
        self.ip = ip
        self.port = port



    def start(self):

        self.modbus_client = ModbusTcpClient(self.ip, port=self.port)

    def close(self):

        self.modbus_client.close()

    def read(self,reg_number,var_type,format = 'CDAB'):
        if var_type == 'int32': value = self.read_int32(reg_number, format=format)
        if var_type == 'uint32':  value = self.read_uint32(reg_number, format=format)
        if var_type == 'uint16':  value = self.read_uint16(reg_number, format=format)
        if var_type == 'int16':  value = self.read_int16(reg_number, format=format)

        return value

    def write(self,value,reg_number,var_type,format = 'CDAB'):
        if var_type == 'int32': self.write_int32(value,reg_number, format=format)
        if var_type == 'uint32': self.write_uint32(value,reg_number, format=format)
        if var_type == 'uint16': self.write_uint16(value,reg_number, format=format)
        if var_type == 'int16': self.write_int16(value,reg_number, format=format)

    def write_int32(self,value, reg_number, format = 'CDAB'):
        # write INT32
        if format == 'CDAB':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)

        builder.add_32bit_int(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_int32(self,reg_number, format = 'CDAB'):
        # read INT32
        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 2)
        if format == 'CDAB':
            decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        value = decoder.decode_32bit_uint()
        return value

    def write_uint32(self,value, reg_number, format = 'CDAB'):
        # write INT32

        if format == 'CDAB':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)

        builder.add_32bit_uint(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_uint32(self,reg_number, format = 'CDAB'):
        # read INT32

        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 2)
        if format == 'CDAB':
            decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        value = decoder.decode_32bit_uint()
        return value
    
    def write_int16(self,value, reg_number, format = 'AB'):
        # write INT32
        if format == 'AB':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)

        builder.add_16bit_int(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_int16(self,reg_number, format = 'AB'):
        # read INT16
        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 1)
        # if format == 'AB':
        #     decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.Big)
        value = modbus_response.registers[0]
        return value

    def write_uint16(self,value, reg_number, format = 'AB'):
        # write INT32
        if format == 'AB':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)

        builder.add_16bit_uint(value)
        builder.to_registers()
        payload = builder.build()
        
        response  = self.modbus_client.write_registers(reg_number, payload,skip_encode=True) 

    def read_uint16(self,reg_number, format = 'AB'):
        # read INT32
        modbus_response = self.modbus_client.read_holding_registers(address = reg_number, count = 2)
        if format == 'AB':
            decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        value = decoder.decode_16bit_uint()
        return value

if __name__ == "__main__":

    ip = "10.0.0.2"
    port = 503

    mb = Modbus_client(ip,port=port)
    mb.start()


    reg_number = 1160
    value = mb.read(reg_number, 'int32', format = 'CDAB')
    print(value)

    # # active powers
    # value = int(2.0e6)
    # reg_number = 40424
    # mb.write(value, reg_number, 'uint32',format = 'CDAB')

    # for port in [510,511,512,513]:
    #     mb = Modbus_client(ip,port=port)
    #     mb.start()

    #     # reactive powers
    #     value = int(0.0e6)
    #     reg_number = 40426
    #     

    # print('Client started')

    # for port in [510,511,512,513]:
    #     mb = Modbus_client(ip,port=port)
    #     mb.start()

    #     # reactive powers
    #     value = int(0.9e6)
    #     reg_number = 40426
    #     mb.write(value, reg_number, 'int32',format = 'CDAB')

    #     # active powers
    #     value = int(2.0e6)
    #     reg_number = 40424
    #     mb.write(value, reg_number, 'uint32',format = 'CDAB')

    # for port in [510,511,512,513]:
    #     mb = Modbus_client(ip,port=port)
    #     mb.start()

    #     # reactive powers
    #     value = int(0.0e6)
    #     reg_number = 40426
    #     value_echo = mb.read(reg_number, 'int32', format = 'CDAB')

    #     print(value_echo/1000)

    # mb = Modbus_client(ip,port=5002)
    # mb.start()
    # reg_number = 372
    # value_echo = mb.read(reg_number, 'int16', format = 'CDAB')
    # print(value_echo/1000)

    

