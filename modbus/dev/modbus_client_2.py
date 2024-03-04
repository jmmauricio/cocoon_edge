
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

ip = "192.168.0.10"
port = 580

modbus_client = ModbusTcpClient(ip, port=port)

reg_number = 2
modbus_response = modbus_client.read_holding_registers(address = reg_number, count = 10)

decoder = BinaryPayloadDecoder.fromRegisters(modbus_response.registers, byteorder=Endian.BIG)
value = decoder.decode_32bit_int()

print(value)
