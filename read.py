'''
# Generator reactive power
PPC python3 read.py -a 10.10.1.1:502 -r 40544 -t int32 

# POI Voltage
PPC python3 read.py -a 10.10.0.3:502 -r 372 -t int32
'''
from modbus.modbus_client import Modbus_client
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-a", help="device ip and port")
parser.add_argument("-r", help="register")
parser.add_argument("-t", help="type")
args = parser.parse_args()

ip, port = args.a.split(':') 
reg_number = int(args.r)
type = args.t

print(ip, port,reg_number)

# ip = "10.0.0.2"
# port = 503
 



mb = Modbus_client(ip,port=port)
mb.start()

value = mb.read(reg_number, type, format = 'CDAB')
print(value)

   
