'''
# Reactive power reference to generator:
PPC python3 write.py -v 2_000_000 -a 10.10.1.1:502 -r 40426 -t int32



'''
from modbus.modbus_client import Modbus_client
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-v", help="value to write")
parser.add_argument("-a", help="device ip and port")
parser.add_argument("-r", help="register")
parser.add_argument("-t", help="type")
args = parser.parse_args()

value = int(args.v)
ip, port = args.a.split(':') 
reg_number = int(args.r)
type = args.t


print(ip, port,reg_number)

mb = Modbus_client(ip,port=port)
mb.start()

mb.write(value, reg_number, type,format = 'CDAB')


mb.close()
   
