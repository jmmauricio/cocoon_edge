from modbus_client import Modbus_client

mb = Modbus_client('10.0.1.1',port=502)
mb.start()
# reactive powers
value = int(0.5e6)
reg_number = 40426
mb.write(value, reg_number, 'int32',format = 'CDAB')

    # ip = "192.168.1.100"
    # port = 510



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